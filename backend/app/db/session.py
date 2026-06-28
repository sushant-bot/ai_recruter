"""Database engine and session helpers."""
from collections.abc import Iterator

from sqlmodel import Session, create_engine

from backend.app.core.settings import settings


engine = create_engine(settings.database_url, echo=settings.debug)


def get_session() -> Iterator[Session]:
    """Yield a database session for dependency injection."""

    with Session(engine) as session:
        yield session
