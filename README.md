# RAG Reliability Engine

An offline-first reference project for measuring retrieval quality before adding an LLM.

Reliable RAG systems need more than plausible answers. This project treats retrieval as a measurable engineering system: documents are chunked, indexed with BM25, queried with citations, and scored against a versioned evaluation set using hit rate, mean reciprocal rank (MRR), precision@k, and citation coverage.

## Why this project exists

A language model cannot recover evidence that retrieval never found. RAG Reliability Engine makes the retrieval layer visible and testable, so engineering teams can compare chunking and ranking choices before spending money on model calls.

## Features

- Pure-Python BM25 index with no model or API key required
- Markdown and text document ingestion
- Paragraph-aware chunking with source metadata
- Search results with stable citations and relevance scores
- Grounded extractive answers for deterministic offline operation
- Evaluation runner with hit rate, MRR, precision@k, and citation coverage
- FastAPI endpoints and an interactive Swagger UI
- Unit tests for chunking, ranking, citations, and evaluation
- Docker support and a GitHub Actions test workflow

## Architecture

```text
documents -> paragraph chunks -> BM25 index
                                  |
question -> tokenizer ------------+-> ranked evidence -> cited answer
                                                        |
evaluation cases ------------------------------------> metrics
```

The answer generator is deliberately extractive. It joins the best evidence sentences and attaches source citations. This keeps behavior deterministic and makes retrieval errors easy to diagnose. An LLM can be added behind the same `SearchResult` contract.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m raglab.cli ask "How does chunk overlap affect retrieval?"
python -m raglab.cli evaluate
```

Run the API:

```bash
uvicorn raglab.api:app --reload
```

Open `http://127.0.0.1:8000/docs`, or query it directly:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Why evaluate retrieval separately?","top_k":3}'
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Example

```text
Question: Why evaluate retrieval separately?

Answer: Retrieval evaluation isolates whether the system found the right evidence before generation begins. [rag-evaluation.md#chunk-1]

Sources:
1. rag-evaluation.md#chunk-1 (score: 4.183)
```

## Evaluation data

`data/eval_cases.json` contains questions and the source documents expected in the top results. Add cases that represent real user questions, especially difficult paraphrases and questions with similar distractor documents.

The included corpus is a compact regression fixture. Its metrics validate the evaluation pipeline and should be replaced with domain-specific documents and cases before a production rollout.

## Project structure

```text
raglab/             retrieval, answer, evaluation, API and CLI modules
data/knowledge/     small Markdown knowledge base
data/eval_cases.json
tests/              offline unit tests
```

## Responsible use

Retrieved text is evidence, not guaranteed truth. Production systems should add authorization checks, document freshness rules, prompt-injection defenses, data governance, and human review for high-impact decisions.

## Roadmap

- Compare BM25 with embedding-based retrieval
- Add reranking and query expansion experiments
- Track latency and retrieval regressions across versions
- Add optional LLM synthesis with faithfulness evaluation

## License

MIT
