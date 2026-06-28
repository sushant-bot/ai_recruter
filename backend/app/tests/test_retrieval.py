"""Retrieval pipeline smoke tests."""
from backend.app.retrieval.rrf import reciprocal_rank_fusion
from backend.app.retrieval.models import RetrievalHit
from backend.app.retrieval.service import HybridRetrievalService


def test_rrf_prefers_consensus_hits() -> None:
    """RRF should place the candidate appearing in both lists first."""

    fused = reciprocal_rank_fusion(
        [
            [RetrievalHit(candidate_id=1, score=0.9, source="faiss")],
            [RetrievalHit(candidate_id=1, score=0.6, source="bm25"), RetrievalHit(candidate_id=2, score=0.5, source="bm25")],
        ]
    )

    assert fused[0].candidate_id == 1


def test_hybrid_retrieval_returns_ranked_hits() -> None:
    """The hybrid retrieval service should return a non-empty ranked list."""

    service = HybridRetrievalService()
    service.index_candidate(1, "python fastapi sqlmodel faiss")
    service.index_candidate(2, "docker kubernetes aws")

    hits = service.search("python fastapi", top_k=2)

    assert hits
    assert hits[0].candidate_id == 1
