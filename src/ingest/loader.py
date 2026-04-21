from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from mdp_agent.models import SourceChunk

SUPPORTED_SUFFIXES = {".txt", ".md"}


def _chunk_text(text: str, chunk_size: int = 120, overlap: int = 20) -> Iterable[str]:
    words = text.split()
    if not words:
        return

    step = max(chunk_size - overlap, 1)
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        if chunk_words:
            yield " ".join(chunk_words)


def ingest_materials(material_dir: Path) -> List[SourceChunk]:
    chunks: List[SourceChunk] = []
    files = sorted(
        p for p in material_dir.glob("**/*") if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )

    for path in files:
        raw = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(_chunk_text(raw), start=1):
            chunk_id = f"{path.name}::chunk_{idx}"
            chunks.append(
                SourceChunk(
                    chunk_id=chunk_id,
                    source_path=str(path),
                    text=chunk,
                )
            )

    return chunks
