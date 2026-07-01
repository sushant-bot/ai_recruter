"""Job description routes."""
from fastapi import APIRouter, Depends

from backend.app.auth.dependencies import rate_limit_request, require_request_access
from backend.app.schemas.job import ParseJDRequest, ParseJDResponse
from backend.app.services.jd_service import JobDescriptionService


router = APIRouter(tags=["jd"], dependencies=[Depends(rate_limit_request), Depends(require_request_access)])
service = JobDescriptionService()


@router.post("/parse-jd", response_model=ParseJDResponse)
def parse_jd(request: ParseJDRequest) -> ParseJDResponse:
    """Parse a job description into a candidate profile."""

    return service.parse(request)
