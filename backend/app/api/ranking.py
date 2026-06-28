"""Candidate ranking routes."""
from fastapi import APIRouter

from backend.app.schemas.common import CandidateDetailResponse
from backend.app.schemas.export import ExportRequest
from backend.app.schemas.ranking import DashboardResponse, RankRequest, RankResponse
from backend.app.schemas.export import ExportResponse
from backend.app.services.candidate_service import CandidateService
from backend.app.services.export_service import ExportService
from backend.app.services.ranking_service import RankingService


router = APIRouter(tags=["ranking"])
ranking_service = RankingService()
candidate_service = CandidateService()
export_service = ExportService()


@router.post("/rank", response_model=RankResponse)
def rank_candidates(request: RankRequest) -> RankResponse:
    """Rank candidate profiles for a job."""

    return ranking_service.rank(request)


@router.get("/candidate/{candidate_id}", response_model=CandidateDetailResponse)
def get_candidate(candidate_id: int) -> CandidateDetailResponse:
    """Return a candidate profile."""

    return candidate_service.get(candidate_id)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard() -> DashboardResponse:
    """Return dashboard data for the default ranking view."""

    return ranking_service.dashboard(RankRequest(job_id=1))


@router.get("/export/csv", response_model=ExportResponse)
def export_csv() -> ExportResponse:
    """Return CSV export metadata."""

    return export_service.csv(ExportRequest(job_id=1))


@router.get("/export/pdf", response_model=ExportResponse)
def export_pdf() -> ExportResponse:
    """Return PDF export metadata."""

    return export_service.pdf(ExportRequest(job_id=1))
