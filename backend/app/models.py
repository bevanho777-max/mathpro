from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class GeneratedProblem(Base):
    __tablename__ = "generated_problems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    problem_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    template_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    grade: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    semester: Mapped[str] = mapped_column(String(16), nullable=False)
    module: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    knowledge_point: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    question_type: Mapped[str] = mapped_column(String(32), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer_rule: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    problem_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("generated_problems.problem_id"),
        index=True,
        nullable=False,
    )
    template_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    grade: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    semester: Mapped[str] = mapped_column(String(16), nullable=False)
    module: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    knowledge_point: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    question_type: Mapped[str] = mapped_column(String(32), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    normalized_answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
