from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.retrieval.hybrid import hybrid_search

router = APIRouter()


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/retrieve/hybrid")
def retrieve_hybrid(
    payload: RetrieveRequest, db: Session = Depends(get_db)
) -> Dict[str, List[Dict[str, Any]]]:
    results = hybrid_search(db=db, query=payload.query, top_k=payload.top_k)
    return {"results": results}
