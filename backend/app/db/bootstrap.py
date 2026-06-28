"""Database bootstrap helpers."""
from collections.abc import Callable

try:  # pragma: no cover - optional dependency in this environment
    from sqlmodel import SQLModel

    from backend.app.db.session import engine
    from backend.app import models  # noqa: F401 - ensure models are imported for metadata registration
except Exception:  # pragma: no cover - keep the application importable without sqlmodel installed
    SQLModel = None
    engine = None


def create_db_and_tables(engine_factory: Callable[[], object] | None = None) -> None:
    """Create all SQLModel tables defined by the backend models.

    A custom engine factory can be supplied in tests.
    """

    if SQLModel is None or engine is None:
        return

    target_engine = engine_factory() if engine_factory is not None else engine
    SQLModel.metadata.create_all(target_engine)
