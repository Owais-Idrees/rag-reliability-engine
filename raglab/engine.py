from pathlib import Path
import re

from .chunking import load_directory
from .retrieval import BM25Index, tokenize


class RAGEngine:
    def __init__(self, knowledge_dir: Path | str):
        self.knowledge_dir = Path(knowledge_dir)
        self.index = BM25Index(load_directory(self.knowledge_dir))

    def search(self, question: str, top_k: int = 3):
        return self.index.search(question, top_k)

    def answer(self, question: str, top_k: int = 3) -> dict:
        results = self.search(question, top_k)
        if not results:
            return {"answer": "I could not find relevant evidence in the knowledge base.", "sources": []}

        query_terms = set(tokenize(question))
        statements: list[str] = []
        for result in results:
            sentences = re.split(r"(?<=[.!?])\s+", result.chunk.text)
            best = max(sentences, key=lambda sentence: len(query_terms.intersection(tokenize(sentence))))
            statements.append(f"{best.strip()} [{result.citation}]")
        return {
            "answer": " ".join(statements),
            "sources": [
                {"citation": result.citation, "source": result.chunk.source, "score": result.score}
                for result in results
            ],
        }
