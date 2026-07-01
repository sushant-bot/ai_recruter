"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.auth.rate_limit import RateLimiter
from backend.app.core.settings import settings
from backend.app.db.bootstrap import create_db_and_tables
from backend.app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables before the application starts serving requests."""

    app.state.rate_limiter = RateLimiter(
        max_requests=settings.rate_limit_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(title="TalentMind AI API", version="1.0.0", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
