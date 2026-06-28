"""Hybrid retrieval pipeline utilities."""

from backend.app.retrieval.bm25 import BM25Retriever
from backend.app.retrieval.embedding import encode_text
from backend.app.retrieval.models import RetrievalHit
from backend.app.retrieval.rrf import reciprocal_rank_fusion
from backend.app.retrieval.service import HybridRetrievalService

__all__ = [
    "BM25Retriever",
    "HybridRetrievalService",
    "RetrievalHit",
    "encode_text",
    "reciprocal_rank_fusion",
]
"""FAISS, BM25, and RRF retrieval modules."""
