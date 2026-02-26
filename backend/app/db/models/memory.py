from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from app.db.session import Base


class SemanticMemory(Base):
    __tablename__ = "semantic_memory"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True, nullable=False)
    value = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    source = Column(String, default="conversation")
    updated_at = Column(DateTime, default=datetime.utcnow)


class EpisodicMemory(Base):
    __tablename__ = "episodic_memory"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)
