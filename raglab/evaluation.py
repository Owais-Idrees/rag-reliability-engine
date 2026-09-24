import json
from pathlib import Path

from .engine import RAGEngine


def evaluate(engine: RAGEngine, cases_path: Path | str, top_k: int = 3) -> dict:
    cases = json.loads(Path(cases_path).read_text(encoding="utf-8"))
    reciprocal_ranks: list[float] = []
    precisions: list[float] = []
    hits = 0
    citation_hits = 0
    details = []

    for case in cases:
        expected = set(case["expected_sources"])
        results = engine.search(case["question"], top_k)
        retrieved = [result.chunk.source for result in results]
        ranks = [index + 1 for index, source in enumerate(retrieved) if source in expected]
        reciprocal_rank = 1 / min(ranks) if ranks else 0.0
        precision = sum(source in expected for source in retrieved) / top_k
        hit = bool(ranks)
        answer = engine.answer(case["question"], top_k)
        cited_sources = {source["source"] for source in answer["sources"]}

        hits += int(hit)
        citation_hits += int(bool(cited_sources.intersection(expected)))
        reciprocal_ranks.append(reciprocal_rank)
        precisions.append(precision)
        details.append({
            "id": case["id"], "hit": hit, "reciprocal_rank": reciprocal_rank,
            "retrieved_sources": retrieved,
        })

    count = len(cases)
    return {
        "cases": count,
        "top_k": top_k,
        "hit_rate": round(hits / count, 4),
        "mrr": round(sum(reciprocal_ranks) / count, 4),
        "precision_at_k": round(sum(precisions) / count, 4),
        "citation_coverage": round(citation_hits / count, 4),
        "details": details,
    }
