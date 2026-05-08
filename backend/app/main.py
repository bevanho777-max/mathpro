from __future__ import annotations

import json
import os
import random
import re
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr


app = FastAPI(title="MathPro API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    return {
        "template_id": template["id"],
        "grade": template["grade"],
        "semester": template["semester"],
        "module": template["module"],
        "knowledge_point": template["knowledge_point"],
        "difficulty": template["difficulty"],
        "question_type": template["question_type"],
        "question": fill(template["question_template"]),
        "answer_rule": fill(template["answer_rule"]),
        "solution": fill(template["solution_template"]),
        "parameters": values,
    }


class AnswerCheckRequest(BaseModel):
    answer: str
    answer_rule: str


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
    return [item["grade"] for item in knowledge_map.get("grades", [])]


@app.get("/api/modules")
def modules(grade: str = Query(...)) -> list[str]:
    knowledge_map = load_knowledge_map()
    for item in knowledge_map.get("grades", []):
        if item["grade"] == grade:
            return [module["name"] for module in item.get("modules", [])]
    raise HTTPException(status_code=404, detail="Grade not found")


@app.get("/api/knowledge-points")
def knowledge_points(grade: str = Query(...), module: str = Query(...)) -> list[dict[str, Any]]:
    knowledge_map = load_knowledge_map()
    for item in knowledge_map.get("grades", []):
        if item["grade"] != grade:
            continue
        for module_item in item.get("modules", []):
            if module_item["name"] == module:
                return module_item.get("knowledge_points", [])
    raise HTTPException(status_code=404, detail="Knowledge points not found")


@app.get("/api/problem/random")
def random_problem(grade: str | None = None, module: str | None = None) -> dict[str, Any]:
    templates = load_templates()
    if grade:
        templates = [item for item in templates if item.get("grade") == grade]
    if module:
        templates = [item for item in templates if item.get("module") == module]
    if not templates:
        raise HTTPException(status_code=404, detail="No templates found")
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
        raise HTTPException(status_code=404, detail="No templates found")
    return render_problem(random.choice(templates))


@app.post("/api/answer/check")
def answer_check(payload: AnswerCheckRequest) -> dict[str, Any]:
    is_correct = check_answer(payload.answer, payload.answer_rule)
    return {"correct": is_correct}


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
