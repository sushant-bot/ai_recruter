"""Generic SQLModel-backed repository implementation."""
from __future__ import annotations

from typing import TypeVar

from backend.app.repositories.base import Repository

try:  # pragma: no cover - optional dependency in this environment
    from sqlmodel import Session, SQLModel, select
except Exception:  # pragma: no cover - keep imports working without sqlmodel installed
    Session = object  # type: ignore[assignment]
    SQLModel = object  # type: ignore[assignment]
    select = None  # type: ignore[assignment]

T = TypeVar("T", bound=SQLModel)


class SQLModelRepository(Repository[T]):
    """Minimal repository for SQLModel entities."""

    def __init__(self, session: Session, model_type: type[T]) -> None:
        if select is None:
            raise RuntimeError("sqlmodel is required to use SQLModelRepository")
        self.session = session
        self.model_type = model_type

    def add(self, item: T) -> T:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get(self, item_id: int) -> T | None:
        statement = select(self.model_type).where(self.model_type.id == item_id)
        return self.session.exec(statement).first()