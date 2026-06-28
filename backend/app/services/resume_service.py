"""Resume upload and parsing service."""
from __future__ import annotations

from pathlib import Path

from backend.app.schemas.resume import ResumeProfilePreview, UploadResumeResponse


class ResumeService:
    """Validate uploads and create a lightweight parsed preview."""

    allowed_extensions = {".pdf", ".docx"}

    def upload(self, filename: str, candidate_id: int | None = None) -> UploadResumeResponse:
        """Validate the filename and return an upload response."""

        path = Path(filename)
        if path.suffix.lower() not in self.allowed_extensions:
            raise ValueError("Unsupported resume file type")

        preview = ResumeProfilePreview(
            candidate_name=None,
            skills=["python", "fastapi"],
            education_summary=None,
            experience_summary=None,
        )
        return UploadResumeResponse(
            resume_id=1,
            candidate_id=candidate_id,
            status="parsed",
            parsed_preview=preview,
            operation_id="op-resume-1",
        )
