from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    source: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float

    @property
    def citation(self) -> str:
        return self.chunk.id
