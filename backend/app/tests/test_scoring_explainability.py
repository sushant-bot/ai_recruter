"""Tests for scoring and explainability scaffolds."""
from backend.app.explainability.service import ExplainabilityService
from backend.app.scoring.service import ScoringService


def test_scoring_service_produces_bounded_final_score() -> None:
    service = ScoringService()

    result = service.score(
        {"skills": ["python", "fastapi", "sqlmodel"], "experience_years": 5},
        {"required_skills": ["python", "fastapi"], "preferred_skills": ["docker"], "experience_years": 4},
        0.72,
    )

    assert 0.0 <= result["final_score"] <= 1.0
    assert result["skill_coverage"] == 1.0
    assert result["experience_match"] == 1.0


def test_explainability_service_reports_strengths_and_gaps() -> None:
    service = ExplainabilityService()

    result = service.explain(
        {"final_score": 0.83, "retrieval": 0.7, "skill_coverage": 1.0, "experience_match": 1.0},
        {"skills": ["python", "fastapi", "sqlmodel"]},
        {"required_skills": ["python", "fastapi", "docker"]},
    )

    assert result["overall_fit"] == "high"
    assert result["strengths"] == ["fastapi", "python"]
    assert result["gaps"] == ["docker"]