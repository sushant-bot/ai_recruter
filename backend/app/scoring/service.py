"""Deterministic scoring scaffold for candidate ranking."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass(frozen=True)
class ScoringWeights:
    """Default weights for the deterministic scoring scaffold."""

    retrieval: float = 0.5
    skill_coverage: float = 0.35
    experience_match: float = 0.15


class ScoringService:
    """Combine retrieval and profile signals into a final score."""

    def __init__(self, weights: ScoringWeights | None = None) -> None:
        self.weights = weights or ScoringWeights()

    def score(self, candidate: dict[str, Any], icp: dict[str, Any], retrieval_score: float) -> dict[str, Any]:
        candidate_skills = {str(skill).lower() for skill in candidate.get("skills", [])}
        required_skills = {str(skill).lower() for skill in icp.get("required_skills", [])}
        preferred_skills = {str(skill).lower() for skill in icp.get("preferred_skills", [])}

        required_overlap = len(candidate_skills & required_skills)
        preferred_overlap = len(candidate_skills & preferred_skills)

        skill_coverage = required_overlap / len(required_skills) if required_skills else 0.5
        preferred_coverage = preferred_overlap / len(preferred_skills) if preferred_skills else 0.5

        candidate_experience = float(candidate.get("experience_years", 0.0) or 0.0)
        required_experience = float(icp.get("experience_years", 0.0) or 0.0)
        experience_match = 1.0 if required_experience <= 0.0 else _clamp(candidate_experience / required_experience)

        normalized_retrieval = _clamp(float(retrieval_score))
        final_score = _clamp(
            (
                normalized_retrieval * self.weights.retrieval
                + skill_coverage * self.weights.skill_coverage
                + experience_match * self.weights.experience_match
            )
        )

        return {
            "retrieval": round(normalized_retrieval, 4),
            "skill_coverage": round(skill_coverage, 4),
            "preferred_coverage": round(preferred_coverage, 4),
            "experience_match": round(experience_match, 4),
            "final_score": round(final_score, 4),
            "weights": {
                "retrieval": self.weights.retrieval,
                "skill_coverage": self.weights.skill_coverage,
                "experience_match": self.weights.experience_match,
            },
        }