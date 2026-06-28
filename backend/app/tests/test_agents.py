"""Tests for the LangGraph workflow scaffold."""
from backend.app.agents.workflow import TalentMindWorkflow, WorkflowPlan
from backend.app.schemas.resume import ResumeProfilePreview, UploadResumeResponse


def test_workflow_plan_has_expected_nodes() -> None:
    workflow = TalentMindWorkflow()

    plan = workflow.build_plan()

    assert isinstance(plan, WorkflowPlan)
    assert plan.entrypoint == "job_understanding"
    assert list(plan.nodes) == ["job_understanding", "resume_parsing", "ranking", "explainability"]
    assert plan.nodes["job_understanding"].next_node == "resume_parsing"
    assert plan.nodes["explainability"].next_node == "__end__"


def test_workflow_run_preserves_state_without_inputs() -> None:
    workflow = TalentMindWorkflow()

    result = workflow.run({"request_id": "req-1"})

    assert result["request_id"] == "req-1"
    assert result["warnings"] == ["ranking was skipped because no rank_request was provided"]
    assert result["errors"] == []


def test_workflow_normalizes_resume_filename_from_windows_path(monkeypatch) -> None:
    workflow = TalentMindWorkflow()
    captured: dict[str, str] = {}

    def fake_upload(filename: str, candidate_id: int | None = None) -> UploadResumeResponse:
        captured["filename"] = filename
        return UploadResumeResponse(
            resume_id=1,
            candidate_id=candidate_id,
            status="parsed",
            parsed_preview=ResumeProfilePreview(candidate_name=None, skills=[], education_summary=None, experience_summary=None),
            operation_id="op-resume-1",
        )

    monkeypatch.setattr(workflow.resume_service, "upload", fake_upload)

    result = workflow.run({"request_id": "req-2", "resume_path": r"C:\\uploads\\candidate.resume.pdf"})

    assert captured["filename"] == "candidate.resume.pdf"
    assert result["resume_response"].status == "parsed"