"""SQLModel definitions for TalentMind AI.

These models follow the design in ARCHITECTURE.md. Keep them minimal; add indices
and constraints when implementing migrations for the target RDBMS.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class JobDescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: Optional[str] = None
    raw_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    icp_json: Optional[str] = None


class Resume(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: Optional[int] = Field(default=None, index=True)
    original_filename: str
    storage_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    parsed_json: Optional[str] = None


class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = Field(default=None, index=True)
    profile_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CandidateEmbedding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(index=True)
    # Production: prefer external vector store; keep a small binary blob for fallback
    vector: Optional[bytes] = None
    model_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RankingResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(index=True)
    candidate_id: int = Field(index=True)
    score: float
    detail_json: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(index=True)
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Education(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(index=True)
    institution: str
    degree: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None


class Experience(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    candidate_id: int = Field(index=True)
    company: str
    title: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    responsibilities: Optional[str] = None


class APILog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    route: str
    method: str
    status_code: int
    request_body: Optional[str] = None
    response_body: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
