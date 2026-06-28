"""Vector store abstraction layer.

Implementations: FAISS-backed, or hosted vector DB adapters.
The scaffold uses an in-memory cosine-similarity store so the backend can be
tested without native FAISS bindings.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, Dict, List, Optional, Protocol


def _cosine_similarity(left: List[float], right: List[float]) -> float:
    """Compute cosine similarity for two equal-length vectors."""

    if len(left) != len(right) or not left:
        return 0.0

    dot_product = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot_product / (left_norm * right_norm)


def encode_text(text: str, dimensions: int = 16) -> List[float]:
    """Encode text into a deterministic low-dimensional vector.

    This is a lightweight stand-in for a real embedding model.
    """

    keywords = [
        "python",
        "fastapi",
        "sql",
        "sqlmodel",
        "faiss",
        "bm25",
        "langgraph",
        "pydantic",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "nlp",
        "llm",
        "recruiter",
    ]
    lowered = text.lower()
    vector = [0.0] * dimensions
    for index, keyword in enumerate(keywords):
        if keyword in lowered:
            vector[index % dimensions] += 1.0
    word_count = max(1, len(lowered.split()))
    vector[-1] = min(1.0, word_count / 100.0)
    return vector


@dataclass(slots=True)
class StoredVector:
    """Persisted in-memory vector record."""

    id: str
    vector: List[float]
    metadata: Dict[str, Any]


class VectorStore(Protocol):
    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a vector to the store."""

    def search(self, vector: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
        """Return list of {id, score, metadata} ordered by score."""

    def remove(self, id: str) -> None:
        """Remove a vector by id."""


class FAISSVectorStore:
    """Minimal FAISS stub implementation.

    Replace with a full implementation in `retrieval/` that depends on `faiss`.
    """

    def __init__(self, index_path: Optional[str] = None) -> None:
        self.index_path = index_path
        self._items: dict[str, StoredVector] = {}

    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        self._items[id] = StoredVector(id=id, vector=list(vector), metadata=metadata or {})

    def search(self, vector: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
        results = [
            {
                "id": item.id,
                "score": _cosine_similarity(vector, item.vector),
                "metadata": item.metadata,
            }
            for item in self._items.values()
        ]
        results.sort(key=lambda result: result["score"], reverse=True)
        return results[:top_k]

    def remove(self, id: str) -> None:
        self._items.pop(id, None)


class InMemoryVectorStore(FAISSVectorStore):
    """Alias for the in-memory scaffold implementation."""

