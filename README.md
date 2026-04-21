# heor-HEmodeling-MDP-AI-agent

v1 Python agent scaffold to generate a **Model Design Plan (MDP)** for a health economic model from source materials.

## What this repo now includes

- End-to-end v1 MDP pipeline:
  - ingest source files (`.txt`, `.md`)
  - retrieve section-relevant content
  - draft structured MDP sections
  - detect missing information
  - generate targeted clarification questions
- JSON schema + markdown template for the MDP format.
- CLI entry point for local execution.
- Example source materials for smoke testing.
- Basic tests.

## Current repository status (initial inspection)
At start of this implementation, the repository only contained a one-line README and no functional code.

## v1 scope
Implemented in this repo:
- ✅ MDP agent only

Explicitly not implemented yet:
- ❌ downstream HE model generation sub-agent
- ❌ parameter-definition sub-agent

## Architecture
See `docs/architecture_overview.md`.

Core modules:
- `src/ingest`
- `src/retrieval`
- `src/gap_check`
- `src/questioning`
- `src/drafting`
- `src/schemas`
- `src/mdp_agent` (pipeline + CLI)

## Install / run

### 1) Create environment and install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Run on example materials
```bash
python -m mdp_agent.cli \
  --materials examples/materials \
  --output examples/output \
  --project-name "Example HEOR MDP"
```

Generated files:
- `examples/output/retrieved_index.json`
- `examples/output/mdp_draft.json`
- `examples/output/mdp_draft.md`

## MDP output structure
Each section has:
- `source_grounded_evidence`
- `agent_synthesis`
- `assumptions`
- `unresolved_gaps`

Required sections are aligned to v1 requirements:
- decision problem
- target population
- intervention and comparators
- perspective
- time horizon
- cycle length
- model structure and rationale
- clinical inputs
- cost inputs
- utility inputs
- assumptions
- validation/uncertainty considerations
- evidence gaps/open questions
- downstream handoff notes

See:
- `docs/mdp_schema.json`
- `docs/mdp_template.md`

## Testing
```bash
PYTHONPATH=src pytest
```

## Practical implementation plan used
1. Add documentation and architecture contract.
2. Add schema/template for structured MDP output.
3. Implement modular ingest → retrieval → drafting → gap-check → questioning pipeline.
4. Add CLI entry point and examples.
5. Add basic tests.

## Next recommended steps
- add PDF/DOCX parsers
- improve retrieval quality (hybrid lexical+vector)
- add interactive clarification loop (ask user and re-draft)
- add export format for downstream sub-agent #2 and #3 handoff
