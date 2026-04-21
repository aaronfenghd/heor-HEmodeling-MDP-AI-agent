from __future__ import annotations

from typing import Dict, List

SECTION_TO_PROMPT = {
    "decision_problem": "Please confirm the precise decision problem, decision context, and jurisdiction.",
    "target_population": "What is the exact target population (line of therapy, inclusion/exclusion, key subgroups)?",
    "intervention_and_comparators": "Please list the intervention and all mandatory comparators for the appraisal context.",
    "perspective": "Which economic perspective should be used (payer, societal, healthcare system)?",
    "time_horizon": "What time horizon should the base case use, and are scenario horizons required?",
    "cycle_length": "What cycle length is preferred and why (clinical relevance vs computational burden)?",
    "model_structure_and_rationale": "Which model structure is preferred and what is the rationale for choosing it?",
    "clinical_inputs": "Which core clinical inputs are required (endpoints, treatment effect sources, extrapolation approach)?",
    "cost_inputs": "Which cost categories and costing sources must be included?",
    "utility_inputs": "What utility framework should be used (instrument, mapping approach, disutilities)?",
    "assumptions": "Please validate key structural/parameter assumptions or provide alternatives.",
    "validation_uncertainty": "Which validation checks and uncertainty analyses are mandatory?",
    "evidence_gaps_open_questions": "Please confirm any known evidence gaps that must be tracked explicitly.",
    "downstream_handoff_notes": "Any specific handoff constraints for coding and parameter-definition sub-agents?",
}


def generate_clarification_questions(gaps: Dict[str, List[str]]) -> List[str]:
    questions: List[str] = []
    for section in gaps:
        prompt = SECTION_TO_PROMPT.get(section)
        if prompt:
            questions.append(prompt)
    return questions
