"""Reciprocal Rank Fusion helpers."""
from __future__ import annotations

from collections import defaultdict

from backend.app.retrieval.models import RetrievalHit


def reciprocal_rank_fusion(result_sets: list[list[RetrievalHit]], k: int = 60) -> list[RetrievalHit]:
    """Fuse multiple ranked retrieval lists using Reciprocal Rank Fusion."""

    fused_scores: dict[int, float] = defaultdict(float)
    sources: dict[int, set[str]] = defaultdict(set)

    for result_set in result_sets:
        for rank, hit in enumerate(result_set, start=1):
            fused_scores[hit.candidate_id] += 1.0 / (k + rank)
            sources[hit.candidate_id].add(hit.source)

    fused_hits = [
        RetrievalHit(candidate_id=candidate_id, score=score, source="rrf", metadata={"sources": sorted(sources[candidate_id])})
        for candidate_id, score in fused_scores.items()
    ]
    fused_hits.sort(key=lambda hit: hit.score, reverse=True)
    return fused_hits
