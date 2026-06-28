"""Service and repository interface definitions.

Keep only typed, minimal contracts here. Implementations live in `services/` and `repositories/`.
"""
from typing import Protocol, List, Dict, Any, Optional


class JDParserInterface(Protocol):
    def parse(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse job description text and return an ICP dict."""


class ResumeParserInterface(Protocol):
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse a resume file and return a structured profile."""


class EmbeddingServiceInterface(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for the provided texts."""


class RetrievalInterface(Protocol):
    def query(self, embedding: List[float], text: Optional[str] = None, top_k: int = 10) -> List[Dict[str, Any]]:
        """Query the retrieval layer and return top candidates with scores."""


class ScoringInterface(Protocol):
    def score(self, candidate: Dict[str, Any], icp: Dict[str, Any], retrieval_score: float) -> Dict[str, Any]:
        """Compute per-factor scores and return a scoring breakdown including final score."""


class ExplainabilityInterface(Protocol):
    def explain(self, scoring_breakdown: Dict[str, Any], candidate: Dict[str, Any], icp: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explainability report JSON for a candidate."""
