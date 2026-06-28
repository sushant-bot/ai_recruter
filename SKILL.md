# SKILL: TalentMind AI — AI Development Guidelines

Summary
-------
This skill codifies the TalentMind AI backend development guidelines and enforces the project's architecture and standards for AI-assisted coding tasks.

Purpose
-------
- Provide a reusable, workspace-scoped `SKILL.md` that instructs agent behavior when contributing to the TalentMind AI backend.
- Ensure all contributions follow Clean Architecture, SOLID principles, type-safety, testing, security, and the fixed retrieval pipeline.

When to use
-----------
- Use this skill before writing or modifying backend code, creating LangGraph workflows, or changing AI prompts and model configs.

What the skill does
-------------------
1. Validates that the requested change aligns with the repository architecture and the fixed retrieval pipeline.
2. Emits a checklist (design → interfaces → implementation → tests → review) to follow before any code is produced.
3. Supplies code-review and testing expectations to the developer or agent.

Core Principles (enforced)
--------------------------
- Clean Architecture; SOLID principles
- Modular code with typed interfaces
- Explicit error handling and logging
- No hardcoded secrets or file paths
- Explainability, security, and performance targets

Repository Conventions
----------------------
- `agents/` — LangGraph nodes and configs only
- `services/` — Business logic
- `repositories/` — DB operations
- `schemas/` — Pydantic request/response models
- `models/` — SQLModel DB models
- `parsers/` — Resume & JD parsing code
- `retrieval/` — FAISS/BM25/RRF implementations
- `ranking/` — Scoring functions and weights
- `explainability/` — Report generation
- `api/` — FastAPI routers
- `utils/` — Reusable helpers
- `tests/` — Unit and integration tests

AI Stack (fixed)
-----------------
- LLMs: Gemini 2.5 Flash (or approved alternative)
- Embeddings: BAAI/bge-large-en-v1.5 or SentenceTransformers
- Parsing: Docling + LLM helpers
- Retrieval: FAISS + rank-bm25 + RRF

Preconditions before implementation
----------------------------------
1. Confirm design & interfaces for the change.
2. Identify relevant modules and existing code to reuse.
3. Specify input/output Pydantic/SQLModel schemas.
4. Draft unit tests (happy path + edge cases) before coding.

Code Review Checklist (automated + manual)
-----------------------------------------
- Syntax and linting (`black`, `ruff`)
- Type checks (`mypy`)
- No missing imports or circular dependencies
- No duplicated logic
- Exceptions handled and mapped to HTTP errors
- Structured logging present for important events
- Unit tests added/updated; 80%+ coverage per module target

Deployment & Security rules
---------------------------
- Secrets in environment variables or secrets manager
- JWT authentication for APIs
- Validate and sanitize uploaded files and inputs
- Rate limit AI calls; circuit-breaker for model endpoints
- Redact PII in logs and exports

Behavioral Rules for Agent
--------------------------
1. Act as Principal Architect first: produce design, interfaces, and tests plan.
2. Ask clarifying questions only when required for correctness.
3. Never start implementation until design and interfaces are approved.
4. After implementation, run tests and perform multi-perspective code review (architecture, backend, AI, security, QA).

Example prompts
---------------
- "Design the DB schema and Pydantic models for Candidate and Resume according to TalentMind conventions." 
- "Draft the LangGraph workflow for JD → Resume parsing → Embeddings → Retrieval → RRF → Scoring." 
- "Review the proposed scoring function for Skill Coverage and return unit tests and edge cases."

Iteration process
-----------------
1. Draft the change plan (design + interfaces + tests).
2. Produce the design doc and ask for approval.
3. Implement module(s) in small, testable increments.
4. Run tests and linting; fix issues.
5. Perform final review from all role perspectives.

Files to update when a module changes
------------------------------------
- `README.md` (module-level)
- `docs/ARCHITECTURE.md` (if architecture-affecting)
- API docs / OpenAPI schemas
- Module-level unit tests

Notes & Constraints
-------------------
- Do not add new architectural components without explicit approval.
- Prioritize deterministic, auditable outputs for explainability.

Contact & Next steps
--------------------
When ready to implement, run: implementers should ask the agent to produce the design artifacts (DB models, API contracts, LangGraph nodes), then approve before coding.
