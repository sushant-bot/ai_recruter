"""Application API router aggregation."""
from fastapi import APIRouter

from backend.app.api.auth import router as auth_router
from backend.app.api.jd import router as jd_router
from backend.app.api.health import router as health_router
from backend.app.api.ranking import router as ranking_router
from backend.app.api.resumes import router as resume_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(jd_router)
api_router.include_router(resume_router)
api_router.include_router(ranking_router)
