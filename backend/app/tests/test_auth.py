"""Tests for auth and rate limiting."""
from backend.app.core.settings import settings
from backend.app.main import create_app
from fastapi.testclient import TestClient


def test_auth_token_and_protected_route_roundtrip(monkeypatch) -> None:
    monkeypatch.setattr(settings, "require_auth", True)
    monkeypatch.setattr(settings, "auth_username", "alice")
    monkeypatch.setattr(settings, "auth_password", type(settings.auth_password)("secret"))
    monkeypatch.setattr(settings, "rate_limit_requests_per_minute", 10)

    client = TestClient(create_app())

    token_response = client.post("/api/v1/auth/token", json={"username": "alice", "password": "secret"})
    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_response.status_code == 200
    assert me_response.json()["subject"] == "alice"

    rank_response = client.post(
        "/api/v1/rank",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"job_id": 1, "top_k": 1},
    )
    assert rank_response.status_code == 200


def test_rate_limit_blocks_repeated_requests(monkeypatch) -> None:
    monkeypatch.setattr(settings, "require_auth", False)
    monkeypatch.setattr(settings, "rate_limit_requests_per_minute", 1)
    monkeypatch.setattr(settings, "rate_limit_window_seconds", 60)

    client = TestClient(create_app())

    first_response = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})
    second_response = client.post("/api/v1/auth/token", json={"username": "admin", "password": "admin"})

    assert first_response.status_code == 200
    assert second_response.status_code == 429