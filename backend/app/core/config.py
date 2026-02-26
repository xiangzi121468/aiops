from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AIOps Evolution Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    CHROMA_PERSIST_DIRECTORY: str = "../data/chromadb"
    SQLITE_URL: str = "sqlite:///../data/sql_app.db"
    
    # OpenAI / LLM
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_PROVIDER: str = "openai"
    
    class Config:
        env_file = ".env"

settings = Settings()

if settings.ENVIRONMENT != "development" and settings.SECRET_KEY == "CHANGE_THIS_IN_PRODUCTION":
    raise ValueError("SECRET_KEY must be set via environment for non-dev use.")

