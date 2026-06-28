"""Health check routes."""
from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a basic health response."""

    return {"status": "ok"}
