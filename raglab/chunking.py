from pathlib import Path
import re

from .models import Chunk


def _paragraphs(text: str) -> list[str]:
    paragraphs = []
    for part in re.split(r"\n\s*\n", text):
        cleaned = re.sub(r"^#{1,6}\s+", "", part.strip())
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if cleaned:
            paragraphs.append(cleaned)
    return paragraphs


def chunk_text(text: str, source: str, max_words: int = 120, overlap_words: int = 20) -> list[Chunk]:
    if max_words < 10 or overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("Require max_words >= 10 and 0 <= overlap_words < max_words")

    chunks: list[Chunk] = []
    buffer: list[str] = []
    for paragraph in _paragraphs(text):
        words = paragraph.split()
        if buffer and len(buffer) + len(words) > max_words:
            chunks.append(Chunk(f"{source}#chunk-{len(chunks) + 1}", source, " ".join(buffer)))
            buffer = buffer[-overlap_words:] if overlap_words else []
        while len(words) > max_words:
            take = max_words - len(buffer)
            buffer.extend(words[:take])
            words = words[take:]
            chunks.append(Chunk(f"{source}#chunk-{len(chunks) + 1}", source, " ".join(buffer)))
            buffer = buffer[-overlap_words:] if overlap_words else []
        buffer.extend(words)

    if buffer:
        chunks.append(Chunk(f"{source}#chunk-{len(chunks) + 1}", source, " ".join(buffer)))
    return chunks


def load_directory(directory: Path, max_words: int = 120, overlap_words: int = 20) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(directory.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        chunks.extend(chunk_text(path.read_text(encoding="utf-8"), path.name, max_words, overlap_words))
    if not chunks:
        raise ValueError(f"No Markdown or text documents found in {directory}")
    return chunks
