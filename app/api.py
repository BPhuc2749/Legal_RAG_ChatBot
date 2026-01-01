from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, List, Optional

from app.pipeline import LegalRAGPipeline
from app.core.logging import get_jsonl_logger, log_event

router = APIRouter()

rag = LegalRAGPipeline()

logger = get_jsonl_logger("app")


class ChatRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class Citation(BaseModel):
    source_type: str
    source: str
    page: Any


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    latency: float


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
   
    request_id = request.state.request_id

    result = rag.run(req.question, top_k=req.top_k)

    # citations 
    citations = []
    seen = set()
    for c in result["contexts"]:
        key = (c["source"], c["page"])
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            {
                "source_type": c["source_type"],
                "source": c["source"],
                "page": c["page"],
            }
        )

    log_event(
        logger,
        {
            "event": "rag_chat",
            "request_id": request_id,
            "question": req.question,
            "top_k": req.top_k,
            "num_citations": len(citations),
            "citations": citations[:10],
            "latency_s": round(result["latency"], 3),
        },
    )

    # trả response cho client + header request id
    return JSONResponse(
        content={
            "answer": result["answer"],
            "citations": citations,
            "latency": result["latency"],
        },
        headers={"x-request-id": request_id},
    )
