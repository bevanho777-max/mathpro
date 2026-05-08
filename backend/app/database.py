from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def database_path() -> Path:
    env_path = os.getenv("MATHPRO_DATABASE_PATH")
    if env_path:
        path = Path(env_path)
        return path if path.is_absolute() else repo_root() / path

    return repo_root() / "local_data" / "mathpro.sqlite3"


def database_url() -> str:
    env_url = os.getenv("MATHPRO_DATABASE_URL")
    if env_url:
        return env_url

    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{path.as_posix()}"


class Base(DeclarativeBase):
    pass


SQLALCHEMY_DATABASE_URL = database_url()
engine_args = {"connect_args": {"check_same_thread": False}} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
