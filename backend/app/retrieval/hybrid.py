from typing import Any, Dict, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models.document import DocumentChunk
from app.retrieval.vector_store import embed_text, get_collection


def keyword_search(db: Session, query: str, limit: int = 5) -> List[Dict[str, Any]]:
    terms = [t for t in query.split() if t]
    if not terms:
        return []

    filters = [DocumentChunk.content.ilike(f"%{term}%") for term in terms]
    rows = (
        db.query(DocumentChunk)
        .filter(or_(*filters))
        .limit(limit)
        .all()
    )

    results = []
    for row in rows:
        hit_score = sum(1 for term in terms if term.lower() in row.content.lower())
        results.append(
            {
                "id": f"kw:{row.id}",
                "content": row.content,
                "source": row.source,
                "score": float(hit_score),
                "method": "keyword",
            }
        )
    return results


def vector_search(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embed_text(query)],
        n_results=limit,
        include=["documents", "metadatas", "distances"],
    )

    output: List[Dict[str, Any]] = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    for idx, doc in enumerate(docs):
        score = 1.0 - float(distances[idx]) if distances else 0.0
        meta = metas[idx] or {}
        output.append(
            {
                "id": f"vec:{idx}",
                "content": doc,
                "source": meta.get("source", "unknown"),
                "score": score,
                "method": "vector",
            }
        )
    return output


def hybrid_search(
    db: Session, query: str, top_k: int = 5
) -> List[Dict[str, Any]]:
    vector_hits = vector_search(query, limit=top_k)
    keyword_hits = keyword_search(db, query, limit=top_k)

    merged: Dict[str, Dict[str, Any]] = {}
    for hit in vector_hits + keyword_hits:
        key = f"{hit['method']}:{hit['content'][:50]}"
        if key not in merged:
            merged[key] = hit
        else:
            merged[key]["score"] = max(merged[key]["score"], hit["score"])

    return sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:top_k]
