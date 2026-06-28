# Software Requirements Specification (SRS)

# TalentMind AI

Version 1.0

---

# 1. Introduction

TalentMind AI is an AI-powered talent intelligence platform that ranks candidates using semantic understanding, hybrid retrieval, and explainable AI.

The objective is to replace traditional keyword-based applicant tracking systems with intelligent candidate evaluation.

---

# 2. Functional Requirements

## FR-1 Job Description Processing

The system shall

* Accept Job Description input
* Parse the description
* Generate an Ideal Candidate Profile
* Extract skills, experience, education and role information

---

## FR-2 Resume Processing

The system shall

* Accept candidate resumes
* Parse PDF/DOCX files
* Extract structured information
* Build candidate profiles

---

## FR-3 Candidate Embedding

The system shall

* Generate dense embeddings
* Store embeddings
* Support semantic retrieval

---

## FR-4 Hybrid Search

The system shall

* Perform semantic retrieval
* Perform lexical BM25 search
* Merge results using Reciprocal Rank Fusion

---

## FR-5 Candidate Ranking

The system shall compute

* Semantic Match
* Skill Coverage
* Career Growth
* Project Quality
* Leadership
* Education
* Certifications
* Domain Experience
* Platform Activity
* Communication Score

The system shall generate a weighted final score.

---

## FR-6 Explainability

The system shall generate

* Overall Fit
* Confidence Score
* Strengths
* Weaknesses
* Missing Skills
* Hiring Recommendation

---

## FR-7 Dashboard

The dashboard shall provide

* Candidate Rankings
* Candidate Details
* Skill Match Charts
* Candidate Comparison
* Recruiter Chat
* CSV Export
* PDF Export

---

## FR-8 API

REST APIs

POST /parse-jd

POST /upload-resume

POST /rank

GET /candidate/{id}

GET /dashboard

GET /export/csv

GET /export/pdf

---

# 3. Non-Functional Requirements

## Performance

* Candidate retrieval < 2 seconds
* Ranking < 5 seconds
* Dashboard load < 3 seconds

---

## Scalability

Support

* 10,000+ resumes
* Multiple concurrent recruiters

---

## Security

* HTTPS
* JWT Authentication
* Secure file uploads
* API rate limiting
* Input validation

---

## Reliability

* Error handling
* Automatic retries
* Logging
* Health monitoring

---

## Maintainability

* Modular architecture
* Typed APIs
* Unit tests
* Documentation

---

## Usability

* Responsive dashboard
* Accessible UI
* Clear explanations
* Minimal learning curve

---

# 4. System Modules

1. Job Understanding Agent
2. Resume Parser Agent
3. Semantic Agent
4. Skill Inference Agent
5. Career Analysis Agent
6. Hybrid Retrieval Engine
7. Multi-Factor Ranking Engine
8. Recruiter Reasoning Agent
9. Explainability Engine
10. Bias Checker
11. Dashboard
12. API Layer

---

# 5. Technology Requirements

## Frontend

* Next.js 15
* React 19
* Tailwind CSS
* shadcn/ui
* Recharts

## Backend

* Python 3.11+
* FastAPI
* Pydantic
* Uvicorn

## AI Stack

* Gemini 2.5 Flash
* LangGraph
* Docling
* Sentence Transformers
* BAAI/bge-large-en-v1.5

## Retrieval

* FAISS
* rank-bm25
* Reciprocal Rank Fusion

## Storage

* Local JSON
* SQLite (development)
* PostgreSQL (production)

---

# 6. Output Requirements

The system shall generate

* Ranked candidate list
* Candidate scores
* Confidence scores
* Explainability report
* CSV output
* PDF hiring report
* REST API responses

---

# 7. Success Criteria

The project will be considered successful if it

* Correctly ranks candidates semantically
* Produces explainable recommendations
* Reduces keyword dependency
* Demonstrates hybrid retrieval
* Generates required submission files
* Achieves competitive evaluation metrics (Precision@K, Recall@K, NDCG@10, MRR)
* Provides an intuitive recruiter dashboard

---

# 8. Future Scope

* Recruiter Feedback Learning Loop
* Neo4j Knowledge Graph
* ATS Integration
* Enterprise Authentication
* Organization-Specific Ranking Models
* Continuous Learning Pipeline
* Multi-Tenant Deployment
* Multilingual Resume Support
