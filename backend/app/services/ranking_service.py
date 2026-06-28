"""Ranking service for candidate scoring."""
from __future__ import annotations

from datetime import datetime, timezone

from backend.app.retrieval.service import HybridRetrievalService
from backend.app.explainability.service import ExplainabilityService
from backend.app.schemas.common import PaginationMeta
from backend.app.schemas.ranking import (
    DashboardAggregates,
    DashboardResponse,
    CandidateFilterSet,
    RankRequest,
    RankResponse,
    RankingResultItem,
    RetrievalSummary,
)
from backend.app.scoring.service import ScoringService


class RankingService:
    """Compute a deterministic ranking response for the current scaffold."""

    def __init__(self) -> None:
        self.retrieval = HybridRetrievalService()
        self.scoring = ScoringService()
        self.explainability = ExplainabilityService()
        self.candidate_profiles: dict[int, dict[str, object]] = {
            101: {"candidate_id": 101, "skills": ["python", "fastapi", "sqlmodel", "faiss", "bm25", "langgraph"], "experience_years": 5},
            102: {"candidate_id": 102, "skills": ["python", "pydantic", "docker", "kubernetes", "aws"], "experience_years": 4},
            103: {"candidate_id": 103, "skills": ["sql", "fastapi", "api", "testing", "logging"], "experience_years": 3},
        }
        for candidate_id, text in {
            101: "python fastapi sqlmodel faiss bm25 langgraph",
            102: "python pydantic docker kubernetes aws",
            103: "sql fastapi api testing logging",
        }.items():
            self.retrieval.index_candidate(candidate_id, text)

    def rank(self, request: RankRequest) -> RankResponse:
        """Produce ranked candidates with a simple heuristic score."""

        query_terms = " ".join(request.filters.required_skills) if request.filters and request.filters.required_skills else f"job {request.job_id}"
        candidate_ids = request.candidate_ids or [101, 102, 103]
        retrieval_hits = [hit for hit in self.retrieval.search(query_terms, top_k=request.top_k) if hit.candidate_id in candidate_ids]
        if not retrieval_hits:
            retrieval_hits = self.retrieval.search(query_terms, top_k=request.top_k)

        icp = {
            "role": f"job-{request.job_id}",
            "required_skills": request.filters.required_skills if request.filters and request.filters.required_skills else query_terms.split(),
            "preferred_skills": [],
            "experience_years": request.filters.min_experience_years if request.filters and request.filters.min_experience_years is not None else 3,
        }

        rankings = [
            self._build_ranking_item(hit.candidate_id, index + 1, hit.score, icp, request.include_explainability)
            for index, hit in enumerate(retrieval_hits[: request.top_k])
        ]
        if not rankings:
            rankings = [
                self._build_fallback_item(candidate_id, index + 1, icp, request.include_explainability)
                for index, candidate_id in enumerate(candidate_ids[: request.top_k])
            ]
        return RankResponse(
            job_id=request.job_id,
            rankings=rankings,
            retrieval_summary=RetrievalSummary(faiss_hits=len(rankings), bm25_hits=len(rankings), rrf_k=60),
            generated_at=datetime.now(timezone.utc),
        )

    def _build_ranking_item(self, candidate_id: int, rank: int, retrieval_score: float, icp: dict[str, object], include_explainability: bool) -> RankingResultItem:
        candidate = self.candidate_profiles.get(candidate_id, {"candidate_id": candidate_id, "skills": [], "experience_years": 0})
        scoring = self.scoring.score(candidate, icp, retrieval_score)
        explainability = self.explainability.explain(scoring, candidate, icp) if include_explainability else None
        return RankingResultItem(
            candidate_id=candidate_id,
            final_score=scoring["final_score"],
            rank=rank,
            breakdown={key: value for key, value in scoring.items() if key != "final_score" and isinstance(value, float)},
            explainability=explainability,
        )

    def _build_fallback_item(self, candidate_id: int, rank: int, icp: dict[str, object], include_explainability: bool) -> RankingResultItem:
        candidate = self.candidate_profiles.get(candidate_id, {"candidate_id": candidate_id, "skills": [], "experience_years": 0})
        scoring = self.scoring.score(candidate, icp, 0.25)
        explainability = self.explainability.explain(scoring, candidate, icp) if include_explainability else None
        return RankingResultItem(
            candidate_id=candidate_id,
            final_score=max(0.1, scoring["final_score"]),
            rank=rank,
            breakdown={key: value for key, value in scoring.items() if key != "final_score" and isinstance(value, float)},
            explainability=explainability,
        )

    def dashboard(self, request: RankRequest) -> DashboardResponse:
        """Build dashboard data from the ranking response."""

        ranking_response = self.rank(request)
        items = ranking_response.rankings
        average_score = sum(item.final_score for item in items) / len(items) if items else 0.0
        top_score = max((item.final_score for item in items), default=0.0)
        return DashboardResponse(
            items=items,
            pagination=PaginationMeta(page=1, page_size=max(1, len(items)), total_items=len(items), total_pages=1),
            aggregates=DashboardAggregates(
                candidate_count=len(items),
                average_score=average_score,
                top_score=top_score,
            ),
        )

