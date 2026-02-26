from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.knowledge.ingestion import ingest_text

router = APIRouter()


class IngestTextRequest(BaseModel):
    source: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


@router.post("/ingest/text")
def ingest_text_endpoint(
    payload: IngestTextRequest, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    return ingest_text(
        db=db,
        source=payload.source,
        content=payload.content,
        metadata=payload.metadata,
    )
