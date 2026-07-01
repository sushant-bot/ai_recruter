#!/usr/bin/env python3
"""Generate a challenge submission from the provided candidate dataset.

This script reads the JSONL candidate dataset, computes a deterministic score
for each profile using dataset-wide rarity plus AI/data relevance signals, and
writes the required CSV with the validator-compatible header:
candidate_id,rank,score,reasoning
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


AI_CORE_TERMS = {
    "ai",
    "machine learning",
    "ml",
    "nlp",
    "llm",
    "rag",
    "embeddings",
    "recommendation systems",
    "fine-tuning llms",
    "prompt engineering",
    "bert",
    "transformer",
    "pytorch",
    "tensorflow",
    "keras",
    "scikit-learn",
    "opencv",
    "asr",
    "speech recognition",
    "gan",
    "forecasting",
    "statistical modeling",
    "feature engineering",
    "data science",
    "mlops",
    "bentoml",
    "haystack",
    "pgvector",
    "opensearch",
    "milvus",
}

DATA_INFRA_TERMS = {
    "python",
    "sql",
    "spark",
    "airflow",
    "dbt",
    "databricks",
    "snowflake",
    "bigquery",
    "kafka",
    "flink",
    "etl",
    "data pipelines",
    "fastapi",
    "flask",
    "django",
    "rest apis",
    "grpc",
    "microservices",
    "docker",
    "kubernetes",
    "terraform",
    "aws",
    "gcp",
    "azure",
    "postgresql",
    "mongodb",
    "redis",
}

LEADERSHIP_TERMS = {"lead", "leader", "manager", "head", "principal", "architect", "owner"}
AI_ROLE_TERMS = {"ai", "ml", "machine learning", "data", "backend", "cloud", "software", "engineer", "scientist", "developer"}


@dataclass(frozen=True)
class CandidateScore:
    candidate_id: str
    score: float
    reasoning: str


@dataclass(frozen=True)
class ScoringContext:
    total_candidates: int
    skill_frequency: Counter[str]
    max_skill_idf: float


def _load_candidates(path: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                candidates.append(json.loads(line))
    return candidates


def _skill_names(candidate: dict[str, Any]) -> list[str]:
    return [str(skill.get("name", "")).strip() for skill in candidate.get("skills", []) if skill.get("name")]


def _collect_scoring_context(candidates: list[dict[str, Any]]) -> ScoringContext:
    skill_frequency: Counter[str] = Counter()
    for candidate in candidates:
        skill_frequency.update({skill.lower() for skill in _skill_names(candidate) if skill})
    total_candidates = len(candidates)
    max_skill_idf = math.log((total_candidates + 1) / 2.0) if total_candidates else 1.0
    return ScoringContext(
        total_candidates=total_candidates,
        skill_frequency=skill_frequency,
        max_skill_idf=max(1e-6, max_skill_idf),
    )


def _sigmoid(value: float, center: float, slope: float) -> float:
    return 1.0 / (1.0 + math.exp(-slope * (value - center)))


def _match_terms(text: str, terms: set[str]) -> int:
    lowered = text.lower()
    return sum(1 for term in terms if term in lowered)


def _skill_rarity_score(skills: list[str], context: ScoringContext) -> float:
    if not skills or context.total_candidates == 0:
        return 0.0
    unique_skills = {skill.lower() for skill in skills if skill}
    idf_total = 0.0
    for skill in unique_skills:
        frequency = context.skill_frequency.get(skill, 0)
        idf_total += math.log((context.total_candidates + 1) / (frequency + 1))
    average_idf = idf_total / len(unique_skills)
    return max(0.0, min(1.0, average_idf / context.max_skill_idf))


def _score_candidate(candidate: dict[str, Any], context: ScoringContext) -> CandidateScore:
    profile = candidate.get("profile", {})
    skills = _skill_names(candidate)
    skill_text = " ".join(skills + [profile.get("headline", ""), profile.get("summary", "")])
    career_history = candidate.get("career_history", [])
    redrob_signals = candidate.get("redrob_signals", {})
    education = candidate.get("education", [])

    years = float(profile.get("years_of_experience", 0.0) or 0.0)
    current_title = str(profile.get("current_title", ""))
    title_text = f"{current_title} {profile.get('headline', '')}"

    core_skill_hits = _match_terms(skill_text, AI_CORE_TERMS)
    infra_skill_hits = _match_terms(skill_text, DATA_INFRA_TERMS)
    title_hits = _match_terms(title_text, AI_ROLE_TERMS)
    leadership_hits = _match_terms(title_text, LEADERSHIP_TERMS)

    rarity_score = _skill_rarity_score(skills, context)
    core_signal = min(1.0, core_skill_hits / 10.0)
    infra_signal = min(1.0, infra_skill_hits / 10.0)
    title_signal = min(1.0, title_hits / 5.0)
    leadership_signal = min(1.0, leadership_hits / 3.0)
    experience_signal = _sigmoid(years, center=4.5, slope=0.45)
    depth_signal = min(1.0, len(skills) / 18.0)
    history_signal = min(1.0, len(career_history) / 4.0)

    engagement_signal = 0.0
    if isinstance(redrob_signals, dict):
        completeness = float(redrob_signals.get("profile_completeness_score", 0.0))
        response_rate = float(redrob_signals.get("recruiter_response_rate", 0.0))
        interview_rate = float(redrob_signals.get("interview_completion_rate", 0.0))
        github_score = float(redrob_signals.get("github_activity_score", -1.0))
        open_to_work = 1.0 if redrob_signals.get("open_to_work_flag", False) else 0.0
        linkedin_connected = 1.0 if redrob_signals.get("linkedin_connected", False) else 0.0

        github_signal = 0.0 if github_score < 0 else github_score / 100.0
        engagement_signal = (
            0.38 * (completeness / 100.0)
            + 0.24 * response_rate
            + 0.12 * interview_rate
            + 0.12 * github_signal
            + 0.08 * open_to_work
            + 0.06 * linkedin_connected
        )

    education_signal = 0.0
    if education:
        tier_bonus = 0.0
        for item in education:
            tier = str(item.get("tier", "unknown")).lower()
            if tier == "tier_1":
                tier_bonus += 1.0
            elif tier == "tier_2":
                tier_bonus += 0.8
            elif tier == "tier_3":
                tier_bonus += 0.55
            elif tier == "tier_4":
                tier_bonus += 0.35
            else:
                tier_bonus += 0.2
        education_signal = min(1.0, tier_bonus / max(1, len(education)))

    score = (
        0.27 * rarity_score
        + 0.24 * core_signal
        + 0.14 * infra_signal
        + 0.10 * title_signal
        + 0.08 * experience_signal
        + 0.07 * depth_signal
        + 0.05 * engagement_signal
        + 0.03 * history_signal
        + 0.02 * leadership_signal
        + 0.01 * education_signal
    )
    score = max(0.0, min(0.9999, round(score, 4)))

    reasoning_bits = []
    if current_title:
        reasoning_bits.append(current_title)
    reasoning_bits.append(f"{years:.1f} yrs")
    reasoning_bits.append(f"{core_skill_hits} core skills")
    reasoning_bits.append(f"{infra_skill_hits} infra skills")
    if isinstance(redrob_signals, dict):
        reasoning_bits.append(f"response rate {float(redrob_signals.get('recruiter_response_rate', 0.0)):.2f}")
    reasoning = "; ".join(reasoning_bits) + "."

    return CandidateScore(candidate_id=str(candidate.get("candidate_id", "")), score=score, reasoning=reasoning)


def generate_submission(candidates_path: Path) -> list[CandidateScore]:
    candidates = _load_candidates(candidates_path)
    context = _collect_scoring_context(candidates)
    scores = [_score_candidate(candidate, context) for candidate in candidates]
    scores.sort(key=lambda item: (-item.score, item.candidate_id))
    return scores[:100]


def write_submission(output_path: Path, scores: list[CandidateScore]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, item in enumerate(scores, start=1):
            writer.writerow([item.candidate_id, rank, f"{item.score:.4f}", item.reasoning])


def _column_name(index: int) -> str:
    name = ""
    current = index
    while current >= 0:
        name = chr((current % 26) + 65) + name
        current = current // 26 - 1
    return name


def _cell_xml(value: Any, row_number: int, column_index: int) -> str:
    cell_reference = f"{_column_name(column_index)}{row_number}"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        cell_value = f"{value:.4f}" if isinstance(value, float) else str(value)
        return f'<c r="{cell_reference}"><v>{cell_value}</v></c>'
    text = str(value)
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    return f'<c r="{cell_reference}" t="inlineStr"><is><t xml:space="preserve">{escaped}</t></is></c>'


def write_submission_xlsx(output_path: Path, scores: list[CandidateScore]) -> None:
    rows = [["candidate_id", "rank", "score", "reasoning"]]
    for rank, item in enumerate(scores, start=1):
        rows.append([item.candidate_id, rank, float(f"{item.score:.4f}"), item.reasoning])

    sheet_rows = []
    for row_number, row in enumerate(rows, start=1):
        cells = "".join(_cell_xml(value, row_number, column_index) for column_index, value in enumerate(row))
        sheet_rows.append(f'<row r="{row_number}">{cells}</row>')

    worksheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData>'
        '</worksheet>'
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="rankings" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )

    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    )

    core_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>TalentMind AI Ranked Candidates</dc:title>'
        '<dc:creator>GitHub Copilot</dc:creator>'
        '<cp:lastModifiedBy>GitHub Copilot</cp:lastModifiedBy>'
        '</cp:coreProperties>'
    )

    app_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Microsoft Excel</Application>'
        '</Properties>'
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml)
        archive.writestr("_rels/.rels", rels_xml)
        archive.writestr("docProps/core.xml", core_xml)
        archive.writestr("docProps/app.xml", app_xml)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        archive.writestr("xl/worksheets/sheet1.xml", worksheet_xml)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a challenge submission from candidates.jsonl")
    parser.add_argument("--candidates", type=Path, required=True, help="Path to the input candidates.jsonl file")
    parser.add_argument("--out", type=Path, required=True, help="Path to write the submission CSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scores = generate_submission(args.candidates)
    if len(scores) < 100:
        raise SystemExit(f"Expected at least 100 candidates, found {len(scores)}")
    if args.out.suffix.lower() == ".xlsx":
        write_submission_xlsx(args.out, scores)
    else:
        write_submission(args.out, scores)


if __name__ == "__main__":
    main()