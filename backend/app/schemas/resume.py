"""Resume ingestion and parsing schemas."""
from pydantic import BaseModel, Field


class ResumeProfilePreview(BaseModel):
    """Preview payload for a parsed resume."""

    candidate_name: str | None = None
    skills: list[str] = Field(default_factory=list)
    education_summary: str | None = None
    experience_summary: str | None = None


class UploadResumeResponse(BaseModel):
    """Response payload for resume upload."""

    resume_id: int
    candidate_id: int | None = None
    status: str
    parsed_preview: ResumeProfilePreview | None = None
    operation_id: str | None = None


class ResumeSummary(BaseModel):
    """Concise resume summary used by dashboard and candidate views."""

    resume_id: int
    original_filename: str
    parsed: bool = False
