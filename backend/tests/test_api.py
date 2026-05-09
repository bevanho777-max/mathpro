from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


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


def teardown_module() -> None:
    engine.dispose()
    _temp_dir.cleanup()


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
