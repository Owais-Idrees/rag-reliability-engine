from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .engine import RAGEngine
from .evaluation import evaluate

ROOT = Path(__file__).resolve().parents[1]
engine = RAGEngine(ROOT / "data" / "knowledge")
app = FastAPI(title="RAG Reliability Engine", version="0.1.0")
WEB = ROOT / "web"
app.mount("/assets", StaticFiles(directory=WEB), name="assets")


class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)


@app.get("/health")
def health():
    return {"status": "ok", "chunks": len(engine.index.chunks), "retriever": "bm25"}


@app.post("/ask")
def ask(request: AskRequest):
    return engine.answer(request.question, request.top_k)


@app.get("/evaluate")
def run_evaluation(top_k: int = 3):
    return evaluate(engine, ROOT / "data" / "eval_cases.json", top_k)


@app.get("/", include_in_schema=False)
def workspace():
    return FileResponse(WEB / "index.html")
