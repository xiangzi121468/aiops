from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agent.graph import build_graph
from app.db.session import get_db

router = APIRouter()


class AgentRunRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/agent/run")
def run_agent(
    payload: AgentRunRequest, db: Session = Depends(get_db)
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
