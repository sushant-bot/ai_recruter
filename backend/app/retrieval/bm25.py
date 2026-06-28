"""Simple BM25-style lexical retrieval.

This is a lightweight in-memory approximation that keeps the project runnable
without external native dependencies.
"""
from __future__ import annotations

from collections import Counter
from math import log

from backend.app.retrieval.models import RetrievalHit


class BM25Retriever:
    """Rank documents based on a BM25-inspired lexical score."""

    def __init__(self) -> None:
        self._documents: dict[int, list[str]] = {}

    def index_document(self, candidate_id: int, text: str) -> None:
        """Add or replace a document in the lexical index."""

        self._documents[candidate_id] = self._tokenize(text)

    def search(self, query_text: str, top_k: int = 10) -> list[RetrievalHit]:
        """Search the lexical index with a query string."""

        query_tokens = self._tokenize(query_text)
        if not query_tokens:
            return []

        query_counts = Counter(query_tokens)
        document_count = max(1, len(self._documents))

        document_frequency: Counter[str] = Counter()
        for tokens in self._documents.values():
            document_frequency.update(set(tokens))

        hits: list[RetrievalHit] = []
        for candidate_id, tokens in self._documents.items():
            token_counts = Counter(tokens)
            score = 0.0
            for token, query_count in query_counts.items():
                if token not in token_counts:
                    continue
                inverse_document_frequency = log((document_count + 1) / (document_frequency[token] + 1)) + 1.0
                score += query_count * token_counts[token] * inverse_document_frequency
            if score > 0.0:
                hits.append(RetrievalHit(candidate_id=candidate_id, score=score, source="bm25", metadata={}))

        hits.sort(key=lambda hit: hit.score, reverse=True)
        return hits[:top_k]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        punctuation = ".,:;!?()[]{}\"'`"
        return [token.strip(punctuation).lower() for token in text.split() if token.strip()]
