from collections import Counter
import math
import re

from .models import Chunk, SearchResult

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        if not chunks:
            raise ValueError("At least one chunk is required")
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.term_counts = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self.lengths = [sum(counts.values()) for counts in self.term_counts]
        self.avg_length = sum(self.lengths) / len(self.lengths)
        document_frequency = Counter()
        for counts in self.term_counts:
            document_frequency.update(counts.keys())
        total = len(chunks)
        self.idf = {
            term: math.log(1 + (total - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        query_terms = tokenize(query)
        scored: list[SearchResult] = []
        for chunk, counts, length in zip(self.chunks, self.term_counts, self.lengths):
            score = 0.0
            for term in query_terms:
                frequency = counts.get(term, 0)
                if not frequency:
                    continue
                normalizer = frequency + self.k1 * (1 - self.b + self.b * length / self.avg_length)
                score += self.idf.get(term, 0.0) * (frequency * (self.k1 + 1)) / normalizer
            if score > 0:
                scored.append(SearchResult(chunk, round(score, 6)))
        return sorted(scored, key=lambda result: (-result.score, result.chunk.id))[:top_k]
