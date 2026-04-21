from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class SourceChunk:
    chunk_id: str
    source_path: str
    text: str


@dataclass
class SectionEvidence:
    section: str
    grounded_points: List[str] = field(default_factory=list)
    source_refs: List[str] = field(default_factory=list)


@dataclass
class MDPSectionDraft:
    section: str
    source_grounded_evidence: List[str] = field(default_factory=list)
    agent_synthesis: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    unresolved_gaps: List[str] = field(default_factory=list)


@dataclass
class PipelineInputs:
    material_dir: Path
    output_dir: Path
    project_name: str = "MDP v1 Draft"


@dataclass
class PipelineArtifacts:
    sections: Dict[str, MDPSectionDraft]
    clarification_questions: List[str]
    retrieved_index_path: Path
    mdp_json_path: Path
    mdp_markdown_path: Path
