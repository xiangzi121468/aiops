from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.memory.service import (
    record_episodic,
    record_semantic,
    recall_episodic,
    recall_semantic,
)

router = APIRouter()


class MemoryRecordRequest(BaseModel):
    type: str
    key: Optional[str] = None
    value: Optional[str] = None
    confidence: float = 1.0
    source: str = "conversation"
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MemoryRecallRequest(BaseModel):
    type: str
    query: Optional[str] = None
    limit: int = 10


@router.post("/memory/record")
def record_memory(
    payload: MemoryRecordRequest, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    if payload.type == "semantic":
        if not payload.key or not payload.value:
            raise HTTPException(status_code=400, detail="key/value required")
        entry = record_semantic(
            db=db,
            key=payload.key,
            value=payload.value,
            confidence=payload.confidence,
            source=payload.source,
        )
        return {"id": entry.id, "type": "semantic"}
    if payload.type == "episodic":
        if not payload.content:
            raise HTTPException(status_code=400, detail="content required")
        entry = record_episodic(
            db=db, content=payload.content, metadata=payload.metadata
        )
        return {"id": entry.id, "type": "episodic"}
    raise HTTPException(status_code=400, detail="unknown memory type")


@router.post("/memory/recall")
def recall_memory(
    payload: MemoryRecallRequest, db: Session = Depends(get_db)
) -> Dict[str, List[Dict[str, Any]]]:
    if payload.type == "semantic":
        rows = recall_semantic(db=db, query=payload.query, limit=payload.limit)
        return {
            "results": [
                {
                    "id": row.id,
                    "key": row.key,
                    "value": row.value,
                    "confidence": row.confidence,
                    "source": row.source,
                }
                for row in rows
            ]
        }
    if payload.type == "episodic":
        rows = recall_episodic(db=db, limit=payload.limit)
        return {
            "results": [
                {
                    "id": row.id,
                    "content": row.content,
                    "metadata_json": row.metadata_json,
                }
                for row in rows
            ]
        }
    raise HTTPException(status_code=400, detail="unknown memory type")
