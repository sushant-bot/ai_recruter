"""Explainability scaffold for ranked candidate results."""
from __future__ import annotations

from typing import Any


class ExplainabilityService:
    """Generate deterministic, structured explanations."""

    def explain(self, scoring_breakdown: dict[str, Any], candidate: dict[str, Any], icp: dict[str, Any]) -> dict[str, Any]:
        required_skills = {str(skill).lower() for skill in icp.get("required_skills", [])}
        candidate_skills = {str(skill).lower() for skill in candidate.get("skills", [])}
        strengths = sorted(candidate_skills & required_skills)
        gaps = sorted(required_skills - candidate_skills)

        final_score = float(scoring_breakdown.get("final_score", 0.0) or 0.0)
        if final_score >= 0.8:
            fit = "high"
        elif final_score >= 0.5:
            fit = "moderate"
        else:
            fit = "low"

        return {
            "overall_fit": fit,
            "summary": f"Candidate matches {len(strengths)} required skills and misses {len(gaps)}.",
            "strengths": strengths,
            "gaps": gaps,
            "signals": {
                "retrieval": scoring_breakdown.get("retrieval", 0.0),
                "skill_coverage": scoring_breakdown.get("skill_coverage", 0.0),
                "experience_match": scoring_breakdown.get("experience_match", 0.0),
            },
            "confidence": round(final_score, 4),
        }