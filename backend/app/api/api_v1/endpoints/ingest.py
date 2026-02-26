from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.knowledge.ingestion import ingest_text

router = APIRouter()


class IngestTextRequest(BaseModel):
    source: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=5000)
    metadata: Optional[Dict[str, Any]] = None


@router.post("/ingest/text")
def ingest_text_endpoint(
    payload: IngestTextRequest,
    db: Session = Depends(get_db),
    _user=Depends(deps.get_current_user),
    _rate=Depends(deps.rate_limit),
) -> Dict[str, Any]:
    return ingest_text(
        db=db,
        source=payload.source,
        content=payload.content,
        metadata=payload.metadata,
    )
