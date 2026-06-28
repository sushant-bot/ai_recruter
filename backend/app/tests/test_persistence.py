"""Tests for the persistence scaffolding."""
import pytest

from backend.app.db.bootstrap import create_db_and_tables
from backend.app.repositories.sqlmodel_repository import SQLModelRepository


def test_create_db_and_tables_accepts_custom_engine() -> None:
    pytest.importorskip("sqlmodel")

    from sqlmodel import SQLModel, create_engine

    engine = create_engine("sqlite:///:memory:")

    create_db_and_tables(lambda: engine)

    assert SQLModel.metadata.tables


def test_sqlmodel_repository_add_and_get_roundtrip() -> None:
    pytest.importorskip("sqlmodel")

    from sqlmodel import Session, SQLModel, create_engine
    from backend.app.models.models import Candidate

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SQLModelRepository(session, Candidate)
        created = repository.add(Candidate(first_name="Ada", last_name="Lovelace", email="ada@example.com"))

        loaded = repository.get(created.id)

    assert loaded is not None
    assert loaded.email == "ada@example.com"