"""API contract smoke tests."""
from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_parse_jd_contract() -> None:
    """The JD parsing contract should return a structured payload."""

    client = TestClient(create_app())
    response = client.post(
        "/api/v1/parse-jd",
        json={"title": "Backend Engineer", "text": "Python FastAPI SQLModel FAISS BM25", "company": "Acme"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["icp"]["role"] == "Backend Engineer"
    assert body["job_id"] == 1


def test_rank_contract() -> None:
    """The ranking endpoint should expose ranked candidates and retrieval metadata."""

    client = TestClient(create_app())
    response = client.post("/api/v1/rank", json={"job_id": 1, "top_k": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["job_id"] == 1
    assert len(body["rankings"]) == 3
