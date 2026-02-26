import hashlib
from typing import List

import chromadb
from app.core.config import settings

_client = None
_collection = None


def _get_client() -> chromadb.Client:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    return _client


def get_collection(name: str = "knowledge"):
    global _collection
    if _collection is None:
        _collection = _get_client().get_or_create_collection(name=name)
    return _collection


def embed_text(text: str, dims: int = 16) -> List[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values = []
    for i in range(dims):
        byte = digest[i]
        values.append(byte / 255.0)
    return values
