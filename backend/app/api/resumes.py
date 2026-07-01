"""Resume ingestion routes."""
from fastapi import APIRouter, Depends, UploadFile

from backend.app.auth.dependencies import rate_limit_request, require_request_access
from backend.app.schemas.resume import UploadResumeResponse
from backend.app.services.resume_service import ResumeService


router = APIRouter(tags=["resumes"], dependencies=[Depends(rate_limit_request), Depends(require_request_access)])
service = ResumeService()


@router.post("/upload-resume", response_model=UploadResumeResponse)
async def upload_resume(file: UploadFile) -> UploadResumeResponse:
    """Validate a resume upload and return a parsed preview."""

    return service.upload(file.filename or "resume.pdf")
