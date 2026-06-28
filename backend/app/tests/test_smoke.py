"""Smoke tests for the backend app shell."""
from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_health_endpoint() -> None:
    """The application should expose a basic health endpoint."""

    client = TestClient(create_app())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
