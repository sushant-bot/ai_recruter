"""Hybrid retrieval service."""
from __future__ import annotations

from backend.app.retrieval.bm25 import BM25Retriever
from backend.app.retrieval.embedding import encode_text
from backend.app.retrieval.models import RetrievalHit
from backend.app.retrieval.rrf import reciprocal_rank_fusion
from backend.app.vector_store import FAISSVectorStore


class HybridRetrievalService:
    """Maintain a lexical and semantic index over candidate profiles."""

    def __init__(self) -> None:
        self.vector_store = FAISSVectorStore()
        self.lexical_store = BM25Retriever()

    def index_candidate(self, candidate_id: int, text: str) -> None:
        """Index a candidate profile for both dense and lexical retrieval."""

        vector = encode_text(text)
        self.vector_store.add(str(candidate_id), vector, metadata={"text": text})
        self.lexical_store.index_document(candidate_id, text)

    def search(self, query_text: str, top_k: int = 10) -> list[RetrievalHit]:
        """Run dense and lexical retrieval and combine the results using RRF."""

        query_vector = encode_text(query_text)
        dense_hits = [
            RetrievalHit(candidate_id=int(hit["id"]), score=float(hit["score"]), source="faiss", metadata=hit["metadata"])
            for hit in self.vector_store.search(query_vector, top_k=top_k)
        ]
        lexical_hits = self.lexical_store.search(query_text, top_k=top_k)
        return reciprocal_rank_fusion([dense_hits, lexical_hits], k=60)[:top_k]
