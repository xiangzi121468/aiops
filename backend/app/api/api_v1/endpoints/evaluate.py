from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.retrieval.hybrid import hybrid_search

router = APIRouter()


class EvalItem(BaseModel):
    query: str
    expected: str


class EvalRequest(BaseModel):
    items: List[EvalItem]
    top_k: int = 5


@router.post("/evaluate/retrieval")
def evaluate_retrieval(
    payload: EvalRequest, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    total = len(payload.items)
    hits = 0
    details = []
    for item in payload.items:
        results = hybrid_search(db=db, query=item.query, top_k=payload.top_k)
        matched = any(item.expected.lower() in r["content"].lower() for r in results)
        if matched:
            hits += 1
        details.append(
            {
                "query": item.query,
                "expected": item.expected,
                "matched": matched,
                "top_k": payload.top_k,
            }
        )
    hit_rate = (hits / total) if total else 0.0
    return {"total": total, "hits": hits, "hit_rate": hit_rate, "details": details}
