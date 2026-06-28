# Design Document

# Project Name

**TalentMind AI**
*An Agentic AI-Powered Candidate Ranking & Talent Intelligence Platform*

---

# 1. Overview

TalentMind AI is an intelligent candidate ranking system designed to overcome the limitations of traditional Applicant Tracking Systems (ATS). Conventional ATS solutions rely heavily on keyword matching, leading to false negatives, keyword stuffing, and poor candidate recommendations.

TalentMind AI understands the intent behind job descriptions, extracts structured candidate information, performs semantic retrieval, reasons over career progression, infers missing skills, and produces explainable candidate rankings.

The platform combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Hybrid Search, Multi-Agent workflows, and Explainable AI (XAI) to simulate how experienced recruiters evaluate candidates.

---

# 2. Design Goals

## Primary Goals

* Understand job requirements semantically.
* Evaluate complete candidate profiles rather than isolated keywords.
* Produce transparent and explainable rankings.
* Minimize recruiter bias.
* Scale efficiently to thousands of resumes.

## Non-Goals (Hackathon Version)

* Fine-tuning custom language models
* Distributed microservices
* Neo4j knowledge graph database
* Reinforcement learning
* Multi-modal resume parsing beyond provided datasets

---

# 3. High-Level Architecture

```text
                        Job Description
                               │
                               ▼
                  ┌────────────────────────┐
                  │ JD Understanding Agent │
                  │ Gemini 2.5 Flash       │
                  └───────────┬────────────┘
                              │
                Structured Ideal Candidate
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Resume Parser Agent    │
                  │ Docling + LLM          │
                  └───────────┬────────────┘
                              │
             Candidate Structured Profile JSON
                              │
        ┌─────────────────────┼──────────────────────┐
        ▼                     ▼                      ▼
 Semantic Agent       Skill Inference Agent    Career Agent
        │                     │                      │
        └─────────────────────┼──────────────────────┘
                              ▼
                  Embedding Generation (BGE)
                              │
                              ▼
               FAISS + BM25 Hybrid Retrieval
                              │
                              ▼
                Reciprocal Rank Fusion (RRF)
                              │
                              ▼
                  Multi-Factor Scoring Engine
                              │
                              ▼
               Recruiter Reasoning Agent (LLM)
                              │
                              ▼
               Explainability + Bias Checker
                              │
                              ▼
                Dashboard + CSV + API Output
```

---

# 4. System Components

## 4.1 Job Understanding Agent

Responsibilities

* Parse Job Description
* Identify mandatory skills
* Extract preferred skills
* Identify experience level
* Detect role type
* Generate structured Ideal Candidate Profile (ICP)

Output

```json
{
  "role": "",
  "required_skills": [],
  "preferred_skills": [],
  "experience": "",
  "industry": "",
  "weights": {}
}
```

---

## 4.2 Resume Parser Agent

Converts resumes into structured JSON.

Extracts

* Skills
* Companies
* Projects
* Education
* Certifications
* Experience
* Career timeline

---

## 4.3 Semantic Agent

Responsible for

* Candidate embeddings
* Job embeddings
* Semantic similarity search

Model

BAAI/bge-large-en-v1.5

---

## 4.4 Skill Inference Agent

Uses LLM reasoning to infer implicit skills.

Example

Input

"Kubernetes, Helm, Istio"

Output

* Docker
* Linux
* Containers
* Cloud Computing
* DevOps

---

## 4.5 Career Analysis Agent

Computes

* Career Growth
* Leadership Progression
* Role Complexity
* Domain Stability

---

## 4.6 Hybrid Retrieval Engine

Combines

* Dense Embeddings
* BM25
* Metadata Filters

Merged using

Reciprocal Rank Fusion (RRF)

---

## 4.7 Multi-Factor Scoring Engine

Final candidate score

| Factor            | Weight |
| ----------------- | ------ |
| Semantic Match    | 35%    |
| Skill Coverage    | 15%    |
| Career Growth     | 10%    |
| Project Quality   | 10%    |
| Leadership        | 10%    |
| Education         | 5%     |
| Certifications    | 5%     |
| Domain Experience | 5%     |
| Platform Activity | 5%     |
| Communication     | 5%     |

---

## 4.8 Recruiter Reasoning Agent

LLM evaluates

* Overall fit
* Missing skills
* Risks
* Strengths
* Recommendation

Returns structured explanations.

---

## 4.9 Explainability Engine

Produces

* Overall Fit Score
* Confidence Score
* Skill Match
* Career Match
* Missing Skills
* Hiring Recommendation

---

## 4.10 Bias Checker

Removes sensitive information before ranking.

Excluded fields

* Name
* Gender
* Age
* Nationality
* Photograph
* Demographic information

---

# 5. Technology Stack

## Frontend

* Next.js 15
* Tailwind CSS
* shadcn/ui
* Recharts

## Backend

* FastAPI

## AI

* Gemini 2.5 Flash
* LangGraph
* Docling
* Sentence Transformers

## Retrieval

* FAISS
* BM25
* Reciprocal Rank Fusion

## Deployment

* Docker
* Railway / Render

---

# 6. Data Flow

1. User uploads Job Description.
2. JD Understanding Agent generates ICP.
3. Candidate resumes are parsed.
4. Candidate profiles are converted into structured JSON.
5. Embeddings are generated.
6. Hybrid Retrieval finds top candidates.
7. RRF merges search results.
8. Multi-Factor Scoring computes suitability.
9. Recruiter Agent reranks candidates.
10. Explainability Engine generates insights.
11. Dashboard visualizes results.
12. CSV/API outputs are generated.

---

# 7. Dashboard Features

* Candidate Rankings
* Skill Match Radar
* Confidence Score
* Explainability Panel
* Candidate Comparison
* Skill Gap Analysis
* Recruiter Copilot
* CSV Export
* PDF Hiring Report

---

# 8. Evaluation Metrics

* Precision@K
* Recall@K
* NDCG@10
* Mean Reciprocal Rank (MRR)
* Response Time
* Ranking Accuracy

---

# 9. Future Enhancements

* Neo4j Knowledge Graph
* Feedback Learning Loop
* Fine-Tuned Ranking Models
* Multi-Language Resume Support
* Organization-Specific Ranking Profiles
* Continuous Learning Pipeline
* ATS Integration
* HR Analytics Dashboard
