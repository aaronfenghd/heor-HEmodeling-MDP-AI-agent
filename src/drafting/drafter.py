from __future__ import annotations

from typing import Iterable, List

from mdp_agent.models import MDPSectionDraft, SourceChunk


def _sentenceize(text: str, max_points: int = 3) -> List[str]:
    fragments = [p.strip() for p in text.replace("\n", " ").split(".")]
    cleaned = [f for f in fragments if len(f.split()) > 6]
    return [f"{c}." for c in cleaned[:max_points]]


def build_section_draft(section: str, hits: Iterable[SourceChunk]) -> MDPSectionDraft:
    evidence: List[str] = []
    source_refs: List[str] = []

    for h in hits:
        points = _sentenceize(h.text, max_points=1)
        for p in points:
            evidence.append(p)
            source_refs.append(f"{h.chunk_id} ({h.source_path})")

    synthesis: List[str] = []
    assumptions: List[str] = []
    gaps: List[str] = []

    if evidence:
        synthesis.append(
            f"Based on retrieved material, this section has {len(evidence)} evidence point(s); a human reviewer should confirm final wording and context."
        )
    else:
        assumptions.append("No direct source evidence retrieved; placeholder assumption inserted for draft continuity.")
        gaps.append("No supporting text retrieved from current materials.")

    if source_refs:
        synthesis.append(f"Traceability references: {', '.join(source_refs[:3])}")

    return MDPSectionDraft(
        section=section,
        source_grounded_evidence=evidence,
        agent_synthesis=synthesis,
        assumptions=assumptions,
        unresolved_gaps=gaps,
    )


def to_markdown(project_name: str, section_drafts: dict[str, MDPSectionDraft], questions: list[str]) -> str:
    lines = [f"# {project_name}", "", "## Structured Model Design Plan Draft", ""]

    for section, draft in section_drafts.items():
        heading = section.replace("_", " ").title()
        lines.extend([f"### {heading}", ""])

        lines.append("**Source-grounded evidence**")
        if draft.source_grounded_evidence:
            lines.extend([f"- {x}" for x in draft.source_grounded_evidence])
        else:
            lines.append("- None retrieved from materials.")

        lines.append("")
        lines.append("**Agent synthesis / reasoning**")
        if draft.agent_synthesis:
            lines.extend([f"- {x}" for x in draft.agent_synthesis])
        else:
            lines.append("- None yet.")

        lines.append("")
        lines.append("**Assumptions**")
        if draft.assumptions:
            lines.extend([f"- {x}" for x in draft.assumptions])
        else:
            lines.append("- None.")

        lines.append("")
        lines.append("**Unresolved gaps / open questions**")
        if draft.unresolved_gaps:
            lines.extend([f"- {x}" for x in draft.unresolved_gaps])
        else:
            lines.append("- None currently flagged.")

        lines.append("")

    lines.extend(["## Clarification Questions", ""])
    if questions:
        lines.extend([f"1. {q}" for q in questions])
    else:
        lines.append("No clarification questions required based on current draft completeness threshold.")

    lines.append("")
    return "\n".join(lines)
