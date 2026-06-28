"""Job description parsing schemas."""
from pydantic import BaseModel, Field


class ParseJDRequest(BaseModel):
    """Request payload for JD parsing."""

    title: str = Field(min_length=1)
    company: str | None = None
    text: str = Field(min_length=1)
    language: str | None = "en"
    source: str | None = None


class JobIdealCandidateProfile(BaseModel):
    """Structured output of the JD understanding step."""

    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience: str | None = None
    weights: dict[str, float] = Field(default_factory=dict)


class ParseJDResponse(BaseModel):
    """Response payload for JD parsing."""

    job_id: int
    icp: JobIdealCandidateProfile
    confidence: float = Field(ge=0.0, le=1.0)
    extracted_skills: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
