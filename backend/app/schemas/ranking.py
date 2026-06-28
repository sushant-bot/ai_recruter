"""Ranking and dashboard schemas."""
from datetime import datetime

from pydantic import BaseModel, Field

from backend.app.schemas.common import PaginationMeta


class CandidateFilterSet(BaseModel):
    """Filters that limit the candidate pool for ranking."""

    min_experience_years: int | None = Field(default=None, ge=0)
    max_experience_years: int | None = Field(default=None, ge=0)
    required_skills: list[str] = Field(default_factory=list)


class RankingResultItem(BaseModel):
    """Single ranked candidate entry."""

    candidate_id: int
    final_score: float = Field(ge=0.0, le=1.0)
    rank: int = Field(ge=1)
    breakdown: dict[str, float] = Field(default_factory=dict)
    explainability: dict[str, object] | None = None


class RetrievalSummary(BaseModel):
    """Summary of dense and lexical retrieval results."""

    faiss_hits: int = Field(ge=0)
    bm25_hits: int = Field(ge=0)
    rrf_k: int = Field(ge=0)


class RankRequest(BaseModel):
    """Request payload for ranking candidates."""

    job_id: int = Field(gt=0)
    candidate_ids: list[int] | None = None
    top_k: int = Field(default=20, ge=1, le=100)
    include_explainability: bool = True
    filters: CandidateFilterSet | None = None


class RankResponse(BaseModel):
    """Response payload for ranking results."""

    job_id: int
    rankings: list[RankingResultItem] = Field(default_factory=list)
    retrieval_summary: RetrievalSummary
    generated_at: datetime


class DashboardAggregates(BaseModel):
    """Aggregated dashboard statistics."""

    candidate_count: int = Field(ge=0)
    average_score: float = Field(ge=0.0, le=1.0)
    top_score: float = Field(ge=0.0, le=1.0)


class DashboardResponse(BaseModel):
    """Dashboard response wrapper."""

    items: list[RankingResultItem] = Field(default_factory=list)
    pagination: PaginationMeta
    aggregates: DashboardAggregates


class OperationStatus(BaseModel):
    """Status for background or queued operations."""

    operation_id: str
    status: str
    message: str | None = None
