from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from drafting import build_section_draft, to_markdown
from gap_check import find_gaps
from ingest import ingest_materials
from questioning import generate_clarification_questions
from retrieval import build_section_queries, retrieve_for_section
from schemas import MDP_SECTION_ORDER

from .models import PipelineArtifacts, PipelineInputs


def run_pipeline(inputs: PipelineInputs) -> PipelineArtifacts:
    inputs.output_dir.mkdir(parents=True, exist_ok=True)

    chunks = ingest_materials(inputs.material_dir)
    query_map = build_section_queries()

    section_drafts = {}
    retrieved_index = {}

    for section in MDP_SECTION_ORDER:
        queries = query_map.get(section, [section.replace("_", " ")])
        hits = retrieve_for_section(chunks, queries, top_k=5)
        section_drafts[section] = build_section_draft(section, hits)
        retrieved_index[section] = [asdict(h) for h in hits]

    gaps = find_gaps(section_drafts)
    questions = generate_clarification_questions(gaps)

    retrieved_index_path = inputs.output_dir / "retrieved_index.json"
    mdp_json_path = inputs.output_dir / "mdp_draft.json"
    mdp_markdown_path = inputs.output_dir / "mdp_draft.md"

    retrieved_index_path.write_text(json.dumps(retrieved_index, indent=2), encoding="utf-8")
    mdp_json_path.write_text(
        json.dumps({k: asdict(v) for k, v in section_drafts.items()}, indent=2),
        encoding="utf-8",
    )
    mdp_markdown_path.write_text(
        to_markdown(inputs.project_name, section_drafts, questions),
        encoding="utf-8",
    )

    return PipelineArtifacts(
        sections=section_drafts,
        clarification_questions=questions,
        retrieved_index_path=retrieved_index_path,
        mdp_json_path=mdp_json_path,
        mdp_markdown_path=mdp_markdown_path,
    )
