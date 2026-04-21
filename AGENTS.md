# Repository Agent Guidance

## Purpose
This repository contains the v1 HEOR MDP agent only.

## Scope guardrails
- Build and maintain only the **MDP agent** here.
- Do not implement downstream HE model generation code yet.
- Do not implement parameter-definition sub-agent logic yet.

## Preferred architecture
- Keep modules separated by pipeline stage:
  - `src/ingest`
  - `src/retrieval`
  - `src/gap_check`
  - `src/questioning`
  - `src/drafting`
  - `src/schemas`
  - `src/mdp_agent` (orchestration + CLI)
- Prefer explicit data classes and JSON outputs for inspectability.

## Coding style
- Prioritize readability and deterministic behavior.
- Avoid hidden side effects and implicit global state.
- Keep dependencies minimal unless justified.

## Output contract
Every MDP section must explicitly separate:
- source-grounded evidence
- agent synthesis/reasoning
- assumptions
- unresolved gaps/open questions

## Validation expectations
When making changes:
- run unit tests with `PYTHONPATH=src pytest`
- run CLI smoke test using example materials
