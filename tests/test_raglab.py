import json
from pathlib import Path
import tempfile
import unittest

from raglab.chunking import chunk_text
from raglab.engine import RAGEngine
from raglab.evaluation import evaluate
from fastapi.testclient import TestClient
from raglab.api import app

ROOT = Path(__file__).resolve().parents[1]


class ChunkingTests(unittest.TestCase):
    def test_chunks_have_stable_citations_and_overlap(self):
        text = " ".join(f"word{i}" for i in range(25))
        chunks = chunk_text(text, "sample.md", max_words=10, overlap_words=2)
        self.assertEqual(chunks[0].id, "sample.md#chunk-1")
        self.assertEqual(chunks[0].text.split()[-2:], chunks[1].text.split()[:2])

    def test_invalid_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            chunk_text("text", "sample.md", max_words=10, overlap_words=10)


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = RAGEngine(ROOT / "data" / "knowledge")

    def test_bm25_returns_expected_source_first(self):
        results = self.engine.search("BM25 lexical ranking document length", top_k=2)
        self.assertEqual(results[0].chunk.source, "bm25.md")

    def test_answer_contains_stable_citation(self):
        result = self.engine.answer("How should access control be enforced before retrieval?", top_k=2)
        self.assertIn("[safety.md#chunk-", result["answer"])
        self.assertEqual(result["sources"][0]["source"], "safety.md")

    def test_unknown_query_returns_no_evidence(self):
        result = self.engine.answer("xylophone zeppelin quasar")
        self.assertEqual(result["sources"], [])

    def test_evaluation_metrics_and_details(self):
        metrics = evaluate(self.engine, ROOT / "data" / "eval_cases.json", top_k=3)
        self.assertEqual(metrics["cases"], 6)
        self.assertGreaterEqual(metrics["hit_rate"], 0.8)
        self.assertEqual(len(metrics["details"]), 6)


class ProductWorkspaceTests(unittest.TestCase):
    def test_workspace_and_health_are_served(self):
        client = TestClient(app)
        self.assertIn("RAG Reliability Engine", client.get("/").text)
        self.assertEqual(client.get("/health").json()["retriever"], "bm25")


if __name__ == "__main__":
    unittest.main()
