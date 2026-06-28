"""Retrieval data models."""
from pydantic import BaseModel, Field


class RetrievalHit(BaseModel):
    """A single ranked retrieval hit."""

    candidate_id: int
    score: float = Field(ge=0.0)
    source: str
    metadata: dict[str, object] = Field(default_factory=dict)
