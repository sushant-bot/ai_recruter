"""Resume ingestion routes."""
from fastapi import APIRouter, UploadFile

from backend.app.schemas.resume import UploadResumeResponse
from backend.app.services.resume_service import ResumeService


router = APIRouter(tags=["resumes"])
service = ResumeService()


@router.post("/upload-resume", response_model=UploadResumeResponse)
async def upload_resume(file: UploadFile) -> UploadResumeResponse:
    """Validate a resume upload and return a parsed preview."""

    return service.upload(file.filename or "resume.pdf")
