"""Background worker/task stubs.

This module contains lightweight stubs for background tasks such as parsing, embedding
generation, and index maintenance. Concrete implementations should use a worker
framework (Celery, RQ, Dramatiq) or FastAPI background tasks depending on deployment.
"""
from typing import Dict, Any


def enqueue_resume_parsing(resume_path: str) -> Dict[str, Any]:
    """Enqueue resume parsing job. Returns a job descriptor.

    In production this should create a task in Celery/RQ and return the task id.
    """

    return {"status": "queued", "path": resume_path}


def enqueue_embedding_generation(items: list) -> Dict[str, Any]:
    """Enqueue embedding generation for a list of text items."""
    return {"status": "queued", "count": len(items)}
