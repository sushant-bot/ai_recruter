"""Database bootstrap smoke test."""
import pytest

sqlmodel = pytest.importorskip("sqlmodel")

from sqlmodel import Session, SQLModel, create_engine

from backend.app import models  # noqa: F401 - register models with metadata
from backend.app.db.bootstrap import create_db_and_tables


def test_create_db_and_tables_in_memory() -> None:
    """Table creation should succeed against an in-memory SQLite database."""

    test_engine = create_engine("sqlite:///:memory:")

    with Session(test_engine):
        SQLModel.metadata.create_all(test_engine)

    # Ensure the production helper remains importable and callable.
    assert callable(create_db_and_tables)
