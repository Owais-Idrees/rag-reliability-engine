import argparse
import json
from pathlib import Path

from .engine import RAGEngine
from .evaluation import evaluate

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="Offline RAG retrieval and evaluation")
    subcommands = parser.add_subparsers(dest="command", required=True)
    ask = subcommands.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=3)
    score = subcommands.add_parser("evaluate")
    score.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    engine = RAGEngine(ROOT / "data" / "knowledge")
    result = engine.answer(args.question, args.top_k) if args.command == "ask" else evaluate(
        engine, ROOT / "data" / "eval_cases.json", args.top_k
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
