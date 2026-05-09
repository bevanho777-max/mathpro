from __future__ import annotations

import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr

from .database import SessionLocal, init_db
from .models import GeneratedProblem, UserAnswer, WrongBook


app = FastAPI(title="MathPro API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NO_TEMPLATES_MESSAGE = "当前范围暂无题目，请换一个知识点或章节。"


@app.on_event("startup")
def startup() -> None:
    init_db()


def data_root() -> Path:
    env_path = os.getenv("MATHPRO_DATA_DIR")
    if env_path:
        return Path(env_path)

    repo_data = Path(__file__).resolve().parents[2] / "data"
    if repo_data.exists():
        return repo_data

    return Path("/app/data")


def load_json(path: Path) -> Any:
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Missing data file: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_knowledge_map() -> dict[str, Any]:
    return load_json(data_root() / "curriculum" / "knowledge_map.json")


def load_templates() -> list[dict[str, Any]]:
    templates: list[dict[str, Any]] = []
    template_dir = data_root() / "templates"
    for path in sorted(template_dir.glob("*.json")):
        payload = load_json(path)
        if isinstance(payload, dict) and "templates" in payload:
            templates.extend(payload["templates"])
        elif isinstance(payload, list):
            templates.extend(payload)
    return templates


def template_scope() -> set[tuple[str, str, str]]:
    return {
        (template["grade"], template["module"], template["knowledge_point"])
        for template in load_templates()
    }


def has_template_for_grade(scope: set[tuple[str, str, str]], grade: str) -> bool:
    return any(item_grade == grade for item_grade, _, _ in scope)


def has_template_for_module(scope: set[tuple[str, str, str]], grade: str, module: str) -> bool:
    return any(item_grade == grade and item_module == module for item_grade, item_module, _ in scope)


def has_template_for_knowledge_point(
    scope: set[tuple[str, str, str]],
    grade: str,
    module: str,
    knowledge_point: str,
) -> bool:
    return (grade, module, knowledge_point) in scope


def save_generated_problem(problem: dict[str, Any], answer_rule: str) -> None:
    with SessionLocal() as session:
        session.add(
            GeneratedProblem(
                problem_id=problem["problem_id"],
                template_id=problem["template_id"],
                grade=problem["grade"],
                semester=problem["semester"],
                module=problem["module"],
                knowledge_point=problem["knowledge_point"],
                difficulty=problem["difficulty"],
                question_type=problem["question_type"],
                question=problem["question"],
                answer_rule=answer_rule,
                solution=problem["solution"],
            )
        )
        session.commit()


def get_generated_problem(problem_id: str) -> GeneratedProblem | None:
    with SessionLocal() as session:
        statement = select(GeneratedProblem).where(GeneratedProblem.problem_id == problem_id)
        return session.execute(statement).scalar_one_or_none()


def save_user_answer(problem: GeneratedProblem, user_answer: str, is_correct: bool) -> UserAnswer:
    normalized_answer = normalize_answer_text(user_answer)
    with SessionLocal() as session:
        answer_record = UserAnswer(
            problem_id=problem.problem_id,
            template_id=problem.template_id,
            grade=problem.grade,
            semester=problem.semester,
            module=problem.module,
            knowledge_point=problem.knowledge_point,
            difficulty=problem.difficulty,
            question_type=problem.question_type,
            user_answer=user_answer,
            is_correct=is_correct,
            normalized_answer=normalized_answer,
        )
        session.add(answer_record)
        session.commit()
        session.refresh(answer_record)
        return answer_record


def answer_record_to_dict(record: UserAnswer) -> dict[str, Any]:
    return {
        "id": record.id,
        "problem_id": record.problem_id,
        "template_id": record.template_id,
        "grade": record.grade,
        "semester": record.semester,
        "module": record.module,
        "knowledge_point": record.knowledge_point,
        "difficulty": record.difficulty,
        "question_type": record.question_type,
        "user_answer": record.user_answer,
        "is_correct": record.is_correct,
        "normalized_answer": record.normalized_answer,
        "created_at": record.created_at.isoformat(),
    }


def record_wrong_answer(problem: GeneratedProblem, user_answer: str) -> bool:
    now = datetime.utcnow()
    with SessionLocal() as session:
        statement = select(WrongBook).where(WrongBook.problem_id == problem.problem_id)
        wrong_record = session.execute(statement).scalar_one_or_none()

        if wrong_record:
            wrong_record.wrong_count += 1
            wrong_record.last_wrong_answer = user_answer
            wrong_record.last_wrong_at = now
            wrong_record.removed = False
            wrong_record.removed_at = None
        else:
            wrong_record = WrongBook(
                problem_id=problem.problem_id,
                template_id=problem.template_id,
                grade=problem.grade,
                semester=problem.semester,
                module=problem.module,
                knowledge_point=problem.knowledge_point,
                difficulty=problem.difficulty,
                question_type=problem.question_type,
                question=problem.question,
                solution=problem.solution,
                first_wrong_answer=user_answer,
                last_wrong_answer=user_answer,
                wrong_count=1,
                removed=False,
                created_at=now,
                last_wrong_at=now,
            )
            session.add(wrong_record)

        session.commit()
        return True


def wrong_book_record_to_dict(record: WrongBook) -> dict[str, Any]:
    return {
        "id": record.id,
        "problem_id": record.problem_id,
        "template_id": record.template_id,
        "grade": record.grade,
        "semester": record.semester,
        "module": record.module,
        "knowledge_point": record.knowledge_point,
        "difficulty": record.difficulty,
        "question_type": record.question_type,
        "question": record.question,
        "solution": record.solution,
        "first_wrong_answer": record.first_wrong_answer,
        "last_wrong_answer": record.last_wrong_answer,
        "wrong_count": record.wrong_count,
        "removed": record.removed,
        "created_at": record.created_at.isoformat(),
        "last_wrong_at": record.last_wrong_at.isoformat(),
        "removed_at": record.removed_at.isoformat() if record.removed_at else None,
    }


def render_problem(template: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for name, spec in template.get("parameters", {}).items():
        if spec.get("type") == "integer":
            candidates = list(range(int(spec["min"]), int(spec["max"]) + 1))
            excluded = set(spec.get("exclude", []))
            candidates = [value for value in candidates if value not in excluded]
            values[name] = random.choice(candidates)
        else:
            values[name] = spec.get("default", "")

    def fill(text: str) -> str:
        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            return str(values.get(key, match.group(0)))

        return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", replace, text)

    answer_rule = fill(template["answer_rule"])
    problem_id = str(uuid4())
    problem = {
        "problem_id": problem_id,
        "template_id": template["id"],
        "grade": template["grade"],
        "semester": template["semester"],
        "module": template["module"],
        "knowledge_point": template["knowledge_point"],
        "difficulty": template["difficulty"],
        "question_type": template["question_type"],
        "question": fill(template["question_template"]),
        "solution": fill(template["solution_template"]),
        "parameters": values,
    }
    save_generated_problem(problem, answer_rule)
    return problem


class AnswerCheckRequest(BaseModel):
    answer: str
    problem_id: str


class WrongBookRemoveRequest(BaseModel):
    problem_id: str


def normalize_answer_text(value: str) -> str:
    replacements = {
        " ": "",
        "\t": "",
        "≥": ">=",
        "≤": "<=",
        "≠": "!=",
        "＝": "=",
        "大于等于": ">=",
        "大于或等于": ">=",
        "不小于": ">=",
        "小于等于": "<=",
        "小于或等于": "<=",
        "不大于": "<=",
        "不等于": "!=",
    }
    normalized = value.strip()
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    return normalized


def check_answer(answer: str, rule: str) -> bool:
    normalized = normalize_answer_text(answer)
    rule = rule.strip()

    if rule.startswith("exact:"):
        return normalized == normalize_answer_text(rule.removeprefix("exact:"))

    if rule.startswith("contains:"):
        return normalize_answer_text(rule.removeprefix("contains:")) in normalized

    if rule.startswith("numeric:"):
        try:
            return abs(float(normalized) - float(rule.removeprefix("numeric:"))) < 1e-9
        except ValueError:
            return False

    if rule.startswith("sympy:"):
        expected = rule.removeprefix("sympy:")
        try:
            return simplify(parse_expr(normalized) - parse_expr(expected)) == 0
        except Exception:
            return False

    return normalized == normalize_answer_text(rule)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "mathpro-backend"}


@app.get("/api/grades")
def grades() -> list[str]:
    knowledge_map = load_knowledge_map()
    scope = template_scope()
    return [
        item["grade"]
        for item in knowledge_map.get("grades", [])
        if has_template_for_grade(scope, item["grade"])
    ]


@app.get("/api/modules")
def modules(grade: str = Query(...)) -> list[str]:
    knowledge_map = load_knowledge_map()
    scope = template_scope()
    for item in knowledge_map.get("grades", []):
        if item["grade"] == grade:
            return [
                module["name"]
                for module in item.get("modules", [])
                if has_template_for_module(scope, grade, module["name"])
            ]
    raise HTTPException(status_code=404, detail="Grade not found")


@app.get("/api/knowledge-points")
def knowledge_points(grade: str = Query(...), module: str = Query(...)) -> list[dict[str, Any]]:
    knowledge_map = load_knowledge_map()
    scope = template_scope()
    for item in knowledge_map.get("grades", []):
        if item["grade"] != grade:
            continue
        for module_item in item.get("modules", []):
            if module_item["name"] == module:
                return [
                    point
                    for point in module_item.get("knowledge_points", [])
                    if has_template_for_knowledge_point(scope, grade, module, point["name"])
                ]
    raise HTTPException(status_code=404, detail="Knowledge points not found")


@app.get("/api/problem/random")
def random_problem(grade: str | None = None, module: str | None = None) -> dict[str, Any]:
    templates = load_templates()
    if grade:
        templates = [item for item in templates if item.get("grade") == grade]
    if module:
        templates = [item for item in templates if item.get("module") == module]
    if not templates:
        raise HTTPException(status_code=404, detail=NO_TEMPLATES_MESSAGE)
    return render_problem(random.choice(templates))


@app.get("/api/problem/by-knowledge")
def problem_by_knowledge(
    grade: str = Query(...),
    module: str = Query(...),
    knowledge_point: str = Query(...),
) -> dict[str, Any]:
    templates = [
        item
        for item in load_templates()
        if item.get("grade") == grade
        and item.get("module") == module
        and item.get("knowledge_point") == knowledge_point
    ]
    if not templates:
        raise HTTPException(status_code=404, detail=NO_TEMPLATES_MESSAGE)
    return render_problem(random.choice(templates))


@app.post("/api/answer/check")
def answer_check(payload: AnswerCheckRequest) -> dict[str, Any]:
    problem_record = get_generated_problem(payload.problem_id)
    if not problem_record:
        raise HTTPException(status_code=404, detail="Generated problem not found")

    is_correct = check_answer(payload.answer, problem_record.answer_rule)
    save_user_answer(problem_record, payload.answer, is_correct)
    wrong_recorded = False
    if not is_correct:
        wrong_recorded = record_wrong_answer(problem_record, payload.answer)

    return {"correct": is_correct, "answer_recorded": True, "wrong_recorded": wrong_recorded}


@app.get("/api/answers/recent")
def recent_answers(limit: int = Query(default=20, ge=1, le=100)) -> list[dict[str, Any]]:
    with SessionLocal() as session:
        statement = select(UserAnswer).order_by(UserAnswer.created_at.desc(), UserAnswer.id.desc()).limit(limit)
        records = session.execute(statement).scalars().all()
        return [answer_record_to_dict(record) for record in records]


@app.get("/api/wrong-book")
def wrong_book(
    limit: int = Query(default=20, ge=1, le=100),
    grade: str | None = None,
    knowledge_point: str | None = None,
) -> list[dict[str, Any]]:
    with SessionLocal() as session:
        statement = select(WrongBook).where(WrongBook.removed.is_(False))
        if grade:
            statement = statement.where(WrongBook.grade == grade)
        if knowledge_point:
            statement = statement.where(WrongBook.knowledge_point == knowledge_point)
        statement = statement.order_by(WrongBook.last_wrong_at.desc(), WrongBook.id.desc()).limit(limit)
        records = session.execute(statement).scalars().all()
        return [wrong_book_record_to_dict(record) for record in records]


@app.post("/api/wrong-book/remove")
def remove_wrong_book_item(payload: WrongBookRemoveRequest) -> dict[str, Any]:
    with SessionLocal() as session:
        statement = select(WrongBook).where(WrongBook.problem_id == payload.problem_id)
        wrong_record = session.execute(statement).scalar_one_or_none()
        if not wrong_record:
            raise HTTPException(status_code=404, detail="Wrong book item not found")

        wrong_record.removed = True
        wrong_record.removed_at = datetime.utcnow()
        session.commit()
        return {"removed": True, "problem_id": payload.problem_id}


@app.get("/api/stats/coverage")
def coverage() -> dict[str, Any]:
    knowledge_map = load_knowledge_map()
    templates = load_templates()
    counts: dict[str, int] = {}
    for template in templates:
        key = "|".join([template["grade"], template["module"], template["knowledge_point"]])
        counts[key] = counts.get(key, 0) + 1

    rows: list[dict[str, Any]] = []
    for grade_item in knowledge_map.get("grades", []):
        for module_item in grade_item.get("modules", []):
            for point in module_item.get("knowledge_points", []):
                key = "|".join([grade_item["grade"], module_item["name"], point["name"]])
                rows.append(
                    {
                        "grade": grade_item["grade"],
                        "module": module_item["name"],
                        "knowledge_point": point["name"],
                        "template_count": counts.get(key, 0),
                    }
                )

    return {"total_knowledge_points": len(rows), "items": rows}
