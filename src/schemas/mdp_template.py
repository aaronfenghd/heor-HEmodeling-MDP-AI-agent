from __future__ import annotations

from typing import Dict, List

MDP_SECTION_ORDER: List[str] = [
    "decision_problem",
    "target_population",
    "intervention_and_comparators",
    "perspective",
    "time_horizon",
    "cycle_length",
    "model_structure_and_rationale",
    "clinical_inputs",
    "cost_inputs",
    "utility_inputs",
    "assumptions",
    "validation_uncertainty",
    "evidence_gaps_open_questions",
    "downstream_handoff_notes",
]


def build_empty_mdp() -> Dict[str, Dict[str, List[str]]]:
    return {
        section: {
            "source_grounded_evidence": [],
            "agent_synthesis": [],
            "assumptions": [],
            "unresolved_gaps": [],
        }
        for section in MDP_SECTION_ORDER
    }


def mdp_schema() -> Dict[str, object]:
    section_template = {
        "type": "object",
        "properties": {
            "source_grounded_evidence": {"type": "array", "items": {"type": "string"}},
            "agent_synthesis": {"type": "array", "items": {"type": "string"}},
            "assumptions": {"type": "array", "items": {"type": "string"}},
            "unresolved_gaps": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "source_grounded_evidence",
            "agent_synthesis",
            "assumptions",
            "unresolved_gaps",
        ],
    }

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Model Design Plan",
        "type": "object",
        "properties": {section: section_template for section in MDP_SECTION_ORDER},
        "required": MDP_SECTION_ORDER,
    }
