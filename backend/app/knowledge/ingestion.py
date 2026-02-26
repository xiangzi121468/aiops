import json
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models.document import DocumentChunk
from app.retrieval.vector_store import get_collection, embed_text


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def ingest_text(
    db: Session,
    source: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata = metadata or {}
    chunks = chunk_text(content)
    collection = get_collection()

    stored_ids: List[str] = []
    for idx, chunk in enumerate(chunks):
        doc_id = str(uuid4())
        stored_ids.append(doc_id)

        meta = {
            "source": source,
            "chunk_index": idx,
            **metadata,
        }

        db_chunk = DocumentChunk(
            source=source,
            content=chunk,
            metadata_json=json.dumps(meta),
        )
        db.add(db_chunk)

        collection.add(
            ids=[doc_id],
            documents=[chunk],
            metadatas=[meta],
            embeddings=[embed_text(chunk)],
        )

    db.commit()
    return {"chunks": len(chunks), "ids": stored_ids}
