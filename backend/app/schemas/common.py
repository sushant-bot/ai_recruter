"""Common API schemas shared across routes."""
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard structured error envelope."""

    code: str = Field(..., examples=["INVALID_INPUT"])
    message: str
    details: dict[str, object] | None = None


class PaginationMeta(BaseModel):
    """Pagination metadata returned by list endpoints."""

    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class SkillSummary(BaseModel):
    """Compact skill summary used in candidate and dashboard views."""

    name: str
    matched: bool = False


class CandidateDetailResponse(BaseModel):
    """Candidate detail response used by the candidate endpoint."""

    candidate_id: int
    full_name: str | None = None
    email: str | None = None
    skills: list[SkillSummary] = Field(default_factory=list)
    latest_rankings: list[dict[str, object]] = Field(default_factory=list)

