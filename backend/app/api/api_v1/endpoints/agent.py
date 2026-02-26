from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api import deps
from app.agent.graph import build_graph
from app.db.session import get_db

router = APIRouter()


class AgentRunRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/agent/run")
def run_agent(
    payload: AgentRunRequest,
    db: Session = Depends(get_db),
    _user=Depends(deps.get_current_user),
    _rate=Depends(deps.rate_limit),
) -> Dict[str, Any]:
    graph = build_graph(db)
    result = graph.invoke(
        {
            "query": payload.query,
            "top_k": payload.top_k,
            "retrieved": [],
            "semantic_memories": [],
            "episodic_memories": [],
            "answer": "",
        }
    )
    return {
        "answer": result["answer"],
        "retrieved": result["retrieved"],
        "semantic_memories": result["semantic_memories"],
        "episodic_memories": result["episodic_memories"],
    }
