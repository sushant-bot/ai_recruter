"""Job description parsing service."""
from __future__ import annotations

from backend.app.schemas.job import JobIdealCandidateProfile, ParseJDRequest, ParseJDResponse


class JobDescriptionService:
    """Produce a structured ICP from a job description using deterministic heuristics."""

    def parse(self, request: ParseJDRequest) -> ParseJDResponse:
        """Build a minimal structured profile from the provided JD."""

        skill_hints = self._extract_skills(request.text)
        icp = JobIdealCandidateProfile(
            role=request.title.strip(),
            required_skills=skill_hints[:5],
            preferred_skills=skill_hints[5:8],
            experience=None,
            weights={
                "semantic_match": 0.35,
                "skill_coverage": 0.15,
                "career_growth": 0.10,
                "project_quality": 0.10,
                "leadership": 0.10,
                "education": 0.05,
                "certifications": 0.05,
                "domain_experience": 0.05,
                "platform_activity": 0.05,
                "communication": 0.05,
            },
        )
        return ParseJDResponse(job_id=1, icp=icp, confidence=0.62, extracted_skills=skill_hints, warnings=[])

    @staticmethod
    def _extract_skills(text: str) -> list[str]:
        """Extract skill-like tokens from the JD text."""

        keywords = [
            "python",
            "fastapi",
            "sql",
            "sqlmodel",
            "faiss",
            "bm25",
            "langgraph",
            "pydantic",
            "docker",
            "kubernetes",
            "aws",
            "gcp",
            "azure",
            "nlp",
            "llm",
        ]
        lowered = text.lower()
        return [keyword for keyword in keywords if keyword in lowered]
