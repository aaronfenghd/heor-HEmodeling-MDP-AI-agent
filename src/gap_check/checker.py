from __future__ import annotations

from typing import Dict, List

from mdp_agent.models import MDPSectionDraft


def find_gaps(section_drafts: Dict[str, MDPSectionDraft], min_grounded_points: int = 1) -> Dict[str, List[str]]:
    gaps: Dict[str, List[str]] = {}
    for section, draft in section_drafts.items():
        section_gaps: List[str] = []
        if len(draft.source_grounded_evidence) < min_grounded_points:
            section_gaps.append("Insufficient source-grounded evidence in this section.")
        if not draft.agent_synthesis:
            section_gaps.append("No synthesis yet; section interpretation is incomplete.")
        if section_gaps:
            gaps[section] = section_gaps
    return gaps
