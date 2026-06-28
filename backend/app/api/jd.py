"""Job description routes."""
from fastapi import APIRouter

from backend.app.schemas.job import ParseJDRequest, ParseJDResponse
from backend.app.services.jd_service import JobDescriptionService


router = APIRouter(tags=["jd"])
service = JobDescriptionService()


@router.post("/parse-jd", response_model=ParseJDResponse)
def parse_jd(request: ParseJDRequest) -> ParseJDResponse:
    """Parse a job description into a candidate profile."""

    return service.parse(request)
