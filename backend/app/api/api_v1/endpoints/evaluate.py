from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.retrieval.hybrid import hybrid_search

router = APIRouter()


class EvalItem(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    expected: str = Field(min_length=1, max_length=500)


class EvalRequest(BaseModel):
    items: List[EvalItem] = Field(min_length=1, max_length=50)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/evaluate/retrieval")
def evaluate_retrieval(
    payload: EvalRequest,
    db: Session = Depends(get_db),
    _user=Depends(deps.get_current_user),
    _rate=Depends(deps.rate_limit),
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
