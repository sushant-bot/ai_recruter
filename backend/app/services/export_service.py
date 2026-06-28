"""Export service for CSV/PDF artifacts."""
from __future__ import annotations

from backend.app.schemas.export import ExportRequest, ExportResponse


class ExportService:
    """Build simple export metadata for the scaffold."""

    def csv(self, request: ExportRequest) -> ExportResponse:
        """Return CSV export metadata."""

        return ExportResponse(filename=f"ranking-job-{request.job_id}.csv", content_type="text/csv")

    def pdf(self, request: ExportRequest) -> ExportResponse:
        """Return PDF export metadata."""

        return ExportResponse(filename=f"ranking-job-{request.job_id}.pdf", content_type="application/pdf")
