from __future__ import annotations

import argparse
from pathlib import Path

from .models import PipelineInputs
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run v1 MDP agent pipeline")
    parser.add_argument("--materials", required=True, help="Directory containing .txt/.md source materials")
    parser.add_argument("--output", required=True, help="Directory where draft artifacts are written")
    parser.add_argument("--project-name", default="HEOR Model Design Plan Draft", help="Name for report heading")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    artifacts = run_pipeline(
        PipelineInputs(
            material_dir=Path(args.materials),
            output_dir=Path(args.output),
            project_name=args.project_name,
        )
    )

    print("MDP draft generated:")
    print(f"- JSON draft: {artifacts.mdp_json_path}")
    print(f"- Markdown draft: {artifacts.mdp_markdown_path}")
    print(f"- Retrieval index: {artifacts.retrieved_index_path}")
    if artifacts.clarification_questions:
        print("- Clarification questions:")
        for q in artifacts.clarification_questions:
            print(f"  * {q}")


if __name__ == "__main__":
    main()
