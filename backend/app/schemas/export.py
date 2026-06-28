"""Export schemas."""
from pydantic import BaseModel


class ExportRequest(BaseModel):
    """Request payload for export operations."""

    job_id: int
    candidate_ids: list[int] | None = None


class ExportResponse(BaseModel):
    """Export metadata response."""

    filename: str
    content_type: str
