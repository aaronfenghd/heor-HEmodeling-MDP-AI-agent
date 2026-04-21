from mdp_agent.models import SourceChunk
from retrieval.simple_retriever import retrieve_for_section


def test_retrieval_prioritizes_matching_chunks() -> None:
    chunks = [
        SourceChunk("1", "a.txt", "This section discusses target population and eligibility criteria."),
        SourceChunk("2", "a.txt", "This section is about budget impact only."),
    ]

    hits = retrieve_for_section(chunks, ["target population", "eligibility"], top_k=1)

    assert len(hits) == 1
    assert hits[0].chunk_id == "1"
