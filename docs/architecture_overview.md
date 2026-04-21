# MDP Agent v1 Architecture Overview

## Goal
Deliver a practical v1 agent that ingests evidence materials and produces a structured Model Design Plan (MDP) draft with explicit traceability, assumptions, and open questions.

## Design principles
- **Simple over clever**: pure-Python, minimal dependencies.
- **Modular**: each workflow stage has a dedicated package.
- **Traceable**: retrieval index and source chunk references are persisted.
- **Interactive-ready**: gap detection generates targeted clarification questions.
- **Future handoff support**: output format has explicit sections for downstream coding and parameter-definition agents.

## Pipeline stages
1. **Ingest (`src/ingest`)**
   - Loads `.txt` and `.md` files from a materials directory.
   - Splits content into overlapping chunks to support retrieval.

2. **Retrieval (`src/retrieval`)**
   - Maps each required MDP section to query terms.
   - Scores chunks via lightweight lexical matching and returns top hits per section.

3. **Drafting (`src/drafting`)**
   - Converts retrieved chunks into section-level structured content:
     - source-grounded evidence
     - agent synthesis
     - assumptions
     - unresolved gaps
   - Emits markdown for review.

4. **Gap Check (`src/gap_check`)**
   - Flags sections with insufficient evidence/synthesis.

5. **Questioning (`src/questioning`)**
   - Generates targeted clarification prompts from detected gaps.

6. **Orchestration (`src/mdp_agent/pipeline.py`)**
   - Runs all steps end-to-end.
   - Writes outputs:
     - `retrieved_index.json`
     - `mdp_draft.json`
     - `mdp_draft.md`

## Output contract for v1
The MDP draft includes all required sections:
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
- validation/uncertainty
- evidence gaps/open questions
- downstream handoff notes

Each section is represented with four explicit fields:
- `source_grounded_evidence`
- `agent_synthesis`
- `assumptions`
- `unresolved_gaps`

## Known v1 limitations
- Retrieval is lexical, not embedding-based.
- Evidence summarization is heuristic.
- No PDF parser in v1 (text/markdown only).
- No conversational memory loop yet (questions are generated as output list).

## Extension path
- Add richer parsers (PDF, DOCX).
- Upgrade retrieval to hybrid lexical + vector search.
- Add chat loop that asks/ingests user clarifications and re-runs affected sections.
- Add structured handoff pack generation for sub-agent #2 and #3.
