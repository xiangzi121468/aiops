import json
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.memory import EpisodicMemory, SemanticMemory


def record_semantic(
    db: Session,
    key: str,
    value: str,
    confidence: float = 1.0,
    source: str = "conversation",
) -> SemanticMemory:
    entry = SemanticMemory(
        key=key,
        value=value,
        confidence=confidence,
        source=source,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def record_episodic(
    db: Session, content: str, metadata: Optional[Dict[str, Any]] = None
) -> EpisodicMemory:
    entry = EpisodicMemory(
        content=content, metadata_json=json.dumps(metadata or {})
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def recall_semantic(
    db: Session, query: Optional[str] = None, limit: int = 10
) -> List[SemanticMemory]:
    q = db.query(SemanticMemory)
    if query:
        q = q.filter(SemanticMemory.key.ilike(f"%{query}%"))
    return q.order_by(SemanticMemory.updated_at.desc()).limit(limit).all()


def recall_episodic(db: Session, limit: int = 10) -> List[EpisodicMemory]:
    return (
        db.query(EpisodicMemory)
        .order_by(EpisodicMemory.created_at.desc())
        .limit(limit)
        .all()
    )
