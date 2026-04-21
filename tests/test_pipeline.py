from pathlib import Path

from mdp_agent.models import PipelineInputs
from mdp_agent.pipeline import run_pipeline


def test_pipeline_generates_outputs(tmp_path: Path) -> None:
    materials = tmp_path / "materials"
    output = tmp_path / "out"
    materials.mkdir()

    (materials / "input.txt").write_text(
        "Decision problem includes reimbursement scope. "
        "Target population includes adults with condition X. "
        "Comparator is standard care. Perspective is payer. "
        "Time horizon lifetime and monthly cycle length are noted. "
        "Clinical inputs include OS and PFS. Costs include drug and follow-up. "
        "Utility inputs include EQ-5D.",
        encoding="utf-8",
    )

    artifacts = run_pipeline(PipelineInputs(material_dir=materials, output_dir=output, project_name="Test"))

    assert artifacts.mdp_json_path.exists()
    assert artifacts.mdp_markdown_path.exists()
    assert artifacts.retrieved_index_path.exists()

    md_text = artifacts.mdp_markdown_path.read_text(encoding="utf-8")
    assert "Structured Model Design Plan Draft" in md_text
    assert "Clarification Questions" in md_text
