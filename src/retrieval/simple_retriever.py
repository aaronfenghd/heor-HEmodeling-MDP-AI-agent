from __future__ import annotations

import re
from collections import Counter
from typing import Dict, Iterable, List, Sequence

from mdp_agent.models import SourceChunk

WORD_RE = re.compile(r"[A-Za-z0-9_\-]+")


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text)]


def build_section_queries() -> Dict[str, List[str]]:
    return {
        "decision_problem": ["decision problem", "scope", "objective", "indication"],
        "target_population": ["population", "eligibility", "subgroup", "baseline"],
        "intervention_and_comparators": ["intervention", "comparator", "standard of care"],
        "perspective": ["perspective", "payer", "societal", "healthcare system"],
        "time_horizon": ["time horizon", "lifetime", "duration"],
        "cycle_length": ["cycle length", "monthly", "weekly", "annual"],
        "model_structure_and_rationale": ["model structure", "markov", "partitioned survival", "rationale"],
        "clinical_inputs": ["clinical input", "efficacy", "survival", "adverse event"],
        "cost_inputs": ["cost", "resource use", "drug acquisition", "administration"],
        "utility_inputs": ["utility", "quality of life", "eq-5d", "disutility"],
        "assumptions": ["assumption", "assume", "scenario"],
        "validation_uncertainty": ["validation", "uncertainty", "sensitivity analysis", "psa"],
        "evidence_gaps_open_questions": ["gap", "limitation", "unknown", "future research"],
        "downstream_handoff_notes": ["implementation", "parameter", "equation", "code"],
    }


def score_chunk(chunk: SourceChunk, query_terms: Sequence[str]) -> int:
    token_counts = Counter(tokenize(chunk.text))
    score = 0
    for term in query_terms:
        parts = tokenize(term)
        if len(parts) == 1:
            score += token_counts.get(parts[0], 0)
        else:
            phrase = " ".join(parts)
            score += chunk.text.lower().count(phrase) * 3
    return score


def retrieve_for_section(
    chunks: Iterable[SourceChunk],
    query_terms: Sequence[str],
    top_k: int = 5,
) -> List[SourceChunk]:
    ranked = []
    for chunk in chunks:
        s = score_chunk(chunk, query_terms)
        if s > 0:
            ranked.append((s, chunk))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in ranked[:top_k]]
