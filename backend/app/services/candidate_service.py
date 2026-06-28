"""Candidate lookup service."""
from __future__ import annotations

from backend.app.schemas.common import CandidateDetailResponse, SkillSummary


class CandidateService:
    """Provide deterministic candidate details for the scaffold."""

    def get(self, candidate_id: int) -> CandidateDetailResponse:
        """Return a structured candidate detail response."""

        return CandidateDetailResponse(
            candidate_id=candidate_id,
            full_name="Sample Candidate",
            email="candidate@example.com",
            skills=[SkillSummary(name="python", matched=True), SkillSummary(name="fastapi", matched=True)],
            latest_rankings=[{"job_id": 1, "score": 0.92}],
        )
