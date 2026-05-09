from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any


BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

_temp_dir = tempfile.TemporaryDirectory()
os.environ["MATHPRO_DATABASE_PATH"] = str(Path(_temp_dir.name) / "mathpro_test.sqlite3")

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)
NO_TEMPLATES_MESSAGE = "当前范围暂无题目，请换一个知识点或章节。"


def teardown_module() -> None:
    engine.dispose()
    _temp_dir.cleanup()


def assert_error_response(response, expected_status: int) -> dict[str, Any]:
    assert response.status_code == expected_status
    assert response.headers["content-type"].startswith("application/json")
    payload = response.json()
    assert "detail" in payload
    assert "answer_rule" not in str(payload)
    return payload


def test_health() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mathpro-backend"}


def test_grades() -> None:
    response = client.get("/api/grades")

    assert response.status_code == 200
    grades = response.json()
    assert "高二" in grades
    assert "高三" in grades


def test_problem_answer_records_and_wrong_book_flow() -> None:
    problem_response = client.get("/api/problem/random", params={"grade": "高三"})

    assert problem_response.status_code == 200
    problem = problem_response.json()
    assert problem["grade"] == "高三"
    assert "problem_id" in problem
    assert "template_id" in problem
    assert "question" in problem
    assert "solution" in problem
    assert "answer_rule" not in problem

    check_response = client.post(
        "/api/answer/check",
        json={"problem_id": problem["problem_id"], "answer": "__wrong_answer__"},
    )

    assert check_response.status_code == 200
    check_result = check_response.json()
    assert check_result["correct"] is False
    assert check_result["answer_recorded"] is True
    assert check_result["wrong_recorded"] is True

    answers_response = client.get("/api/answers/recent", params={"limit": 5})

    assert answers_response.status_code == 200
    answers = answers_response.json()
    assert any(item["problem_id"] == problem["problem_id"] for item in answers)

    wrong_book_response = client.get("/api/wrong-book", params={"limit": 5})

    assert wrong_book_response.status_code == 200
    wrong_items = wrong_book_response.json()
    wrong_item = next(item for item in wrong_items if item["problem_id"] == problem["problem_id"])
    assert wrong_item["last_wrong_answer"] == "__wrong_answer__"
    assert wrong_item["wrong_count"] == 1
    assert wrong_item["removed"] is False

    remove_response = client.post("/api/wrong-book/remove", json={"problem_id": problem["problem_id"]})

    assert remove_response.status_code == 200
    assert remove_response.json() == {"removed": True, "problem_id": problem["problem_id"]}

    wrong_book_after_remove_response = client.get("/api/wrong-book", params={"limit": 5})

    assert wrong_book_after_remove_response.status_code == 200
    wrong_items_after_remove = wrong_book_after_remove_response.json()
    assert all(item["problem_id"] != problem["problem_id"] for item in wrong_items_after_remove)


def test_answer_check_rejects_missing_or_unknown_problem() -> None:
    unknown_response = client.post(
        "/api/answer/check",
        json={"problem_id": "missing-problem-id", "answer": "A"},
    )
    unknown_payload = assert_error_response(unknown_response, 404)
    assert unknown_payload["detail"] == "Generated problem not found"

    missing_problem_id_response = client.post("/api/answer/check", json={"answer": "A"})
    missing_problem_id_payload = assert_error_response(missing_problem_id_response, 422)
    assert "problem_id" in str(missing_problem_id_payload["detail"])

    missing_answer_response = client.post("/api/answer/check", json={"problem_id": "missing-problem-id"})
    missing_answer_payload = assert_error_response(missing_answer_response, 422)
    assert "answer" in str(missing_answer_payload["detail"])


def test_problem_random_returns_friendly_message_for_unknown_scope() -> None:
    unknown_grade_response = client.get("/api/problem/random", params={"grade": "不存在年级"})
    unknown_grade_payload = assert_error_response(unknown_grade_response, 404)
    assert unknown_grade_payload["detail"] == NO_TEMPLATES_MESSAGE

    unknown_module_response = client.get(
        "/api/problem/random",
        params={"grade": "高三", "module": "不存在章节"},
    )
    unknown_module_payload = assert_error_response(unknown_module_response, 404)
    assert unknown_module_payload["detail"] == NO_TEMPLATES_MESSAGE

    unknown_knowledge_point_response = client.get(
        "/api/problem/random",
        params={"grade": "高三", "module": "高考专题", "knowledge_point": "不存在知识点"},
    )
    unknown_knowledge_point_payload = assert_error_response(unknown_knowledge_point_response, 404)
    assert unknown_knowledge_point_payload["detail"] == NO_TEMPLATES_MESSAGE


def test_scope_lookup_rejects_unknown_grade() -> None:
    modules_response = client.get("/api/modules", params={"grade": "不存在年级"})
    modules_payload = assert_error_response(modules_response, 404)
    assert modules_payload["detail"] == "Grade not found"

    knowledge_points_response = client.get(
        "/api/knowledge-points",
        params={"grade": "不存在年级", "module": "函数"},
    )
    knowledge_points_payload = assert_error_response(knowledge_points_response, 404)
    assert knowledge_points_payload["detail"] == "Knowledge points not found"


def test_limit_boundaries_return_json_errors() -> None:
    for path in ["/api/answers/recent", "/api/wrong-book"]:
        low_response = client.get(path, params={"limit": 0})
        low_payload = assert_error_response(low_response, 422)
        assert "limit" in str(low_payload["detail"])

        high_response = client.get(path, params={"limit": 999})
        high_payload = assert_error_response(high_response, 422)
        assert "limit" in str(high_payload["detail"])


def test_wrong_book_remove_rejects_missing_or_unknown_problem() -> None:
    unknown_response = client.post("/api/wrong-book/remove", json={"problem_id": "missing-problem-id"})
    unknown_payload = assert_error_response(unknown_response, 404)
    assert unknown_payload["detail"] == "Wrong book item not found"

    missing_problem_id_response = client.post("/api/wrong-book/remove", json={})
    missing_problem_id_payload = assert_error_response(missing_problem_id_response, 422)
    assert "problem_id" in str(missing_problem_id_payload["detail"])
