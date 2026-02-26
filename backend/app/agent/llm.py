from typing import Optional

from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_llm() -> Optional[ChatOpenAI]:
    if settings.LLM_PROVIDER != "openai":
        return None
    if not settings.OPENAI_API_KEY:
        return None
    return ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY)
