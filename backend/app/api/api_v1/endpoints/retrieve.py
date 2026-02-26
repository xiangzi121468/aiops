from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.retrieval.hybrid import hybrid_search

router = APIRouter()


class RetrieveRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/retrieve/hybrid")
def retrieve_hybrid(
    payload: RetrieveRequest,
    db: Session = Depends(get_db),
    _user=Depends(deps.get_current_user),
    _rate=Depends(deps.rate_limit),
) -> Dict[str, List[Dict[str, Any]]]:
    results = hybrid_search(db=db, query=payload.query, top_k=payload.top_k)
    return {"results": results}
