"""Typed LangGraph workflow stubs for the TalentMind pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, TypedDict

try:  # pragma: no cover - optional dependency for future expansion
    from langgraph.graph import END, StateGraph
except Exception:  # pragma: no cover - the scaffold must work without langgraph installed
    END = "__end__"
    StateGraph = None

from backend.app.schemas.job import ParseJDRequest, ParseJDResponse
from backend.app.schemas.ranking import RankRequest, RankResponse
from backend.app.schemas.resume import UploadResumeResponse
from backend.app.services.jd_service import JobDescriptionService
from backend.app.services.ranking_service import RankingService
from backend.app.services.resume_service import ResumeService


class WorkflowState(TypedDict, total=False):
    """Shared workflow state passed between nodes."""

    request_id: str
    jd_request: ParseJDRequest
    jd_response: ParseJDResponse
    resume_path: str
    resume_filename: str
    resume_response: UploadResumeResponse
    rank_request: RankRequest
    rank_response: RankResponse
    warnings: list[str]
    errors: list[str]


@dataclass(frozen=True)
class WorkflowNodeSpec:
    """Definition for a workflow node and its outgoing edge."""

    name: str
    description: str
    handler: Callable[[WorkflowState], WorkflowState]
    next_node: str | None = None


@dataclass(frozen=True)
class WorkflowPlan:
    """A lightweight, inspectable workflow plan."""

    entrypoint: str
    nodes: dict[str, WorkflowNodeSpec] = field(default_factory=dict)
    end_node: str = END


class TalentMindWorkflow:
    """Orchestrates the TalentMind pipeline as a typed workflow stub."""

    def __init__(self) -> None:
        self.jd_service = JobDescriptionService()
        self.resume_service = ResumeService()
        self.ranking_service = RankingService()

    def build_plan(self) -> WorkflowPlan:
        """Return the static workflow plan used by the scaffold."""

        return WorkflowPlan(
            entrypoint="job_understanding",
            nodes={
                "job_understanding": WorkflowNodeSpec(
                    name="job_understanding",
                    description="Parse the job description into an ICP.",
                    handler=self._job_understanding,
                    next_node="resume_parsing",
                ),
                "resume_parsing": WorkflowNodeSpec(
                    name="resume_parsing",
                    description="Validate and stage the resume payload.",
                    handler=self._resume_parsing,
                    next_node="ranking",
                ),
                "ranking": WorkflowNodeSpec(
                    name="ranking",
                    description="Rank candidates using the retrieval-backed service.",
                    handler=self._ranking,
                    next_node="explainability",
                ),
                "explainability": WorkflowNodeSpec(
                    name="explainability",
                    description="Attach explainability details for downstream consumers.",
                    handler=self._explainability,
                    next_node=END,
                ),
            },
        )

    def compile(self) -> Any:
        """Compile a LangGraph workflow when the dependency is available."""

        plan = self.build_plan()
        if StateGraph is None:
            return plan

        graph = StateGraph(WorkflowState)
        for node in plan.nodes.values():
            graph.add_node(node.name, node.handler)

        graph.set_entry_point(plan.entrypoint)
        for node in plan.nodes.values():
            if node.next_node is not None:
                graph.add_edge(node.name, node.next_node)

        return graph.compile()

    def run(self, state: WorkflowState) -> WorkflowState:
        """Execute the scaffold sequentially without requiring LangGraph."""

        current_state = dict(state)
        plan = self.build_plan()
        for node_name in plan.nodes:
            current_state = plan.nodes[node_name].handler(current_state)
        return current_state

    def _job_understanding(self, state: WorkflowState) -> WorkflowState:
        if "jd_request" not in state:
            return state
        current = dict(state)
        current["jd_response"] = self.jd_service.parse(state["jd_request"])
        return current

    def _resume_parsing(self, state: WorkflowState) -> WorkflowState:
        current = dict(state)
        resume_path = state.get("resume_path")
        resume_filename = state.get("resume_filename") or self._normalize_filename(resume_path)
        if resume_path is not None:
            current["resume_response"] = self.resume_service.upload(resume_filename)
        return current

    def _ranking(self, state: WorkflowState) -> WorkflowState:
        current = dict(state)
        if "rank_request" in state:
            current["rank_response"] = self.ranking_service.rank(state["rank_request"])
        return current

    def _explainability(self, state: WorkflowState) -> WorkflowState:
        current = dict(state)
        current.setdefault("warnings", [])
        current.setdefault("errors", [])
        if "rank_response" not in current:
            current["warnings"].append("ranking was skipped because no rank_request was provided")
        return current

    @staticmethod
    def _normalize_filename(resume_path: str | None) -> str:
        if not resume_path:
            return "resume.pdf"
        return Path(resume_path).name or "resume.pdf"


def build_talentmind_workflow() -> Any:
    """Return a compiled workflow when possible, otherwise the plan."""

    return TalentMindWorkflow().compile()