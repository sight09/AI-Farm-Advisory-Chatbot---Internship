# services/database/schemas.py
from sqlalchemy import Column, Integer, Text, JSON, DateTime, func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    doc_metadata = Column(JSON, nullable=True)
    # EMBED_DIM is read from config at runtime when creating table
    embedding = Column(Vector(int(ENV_EMBED_DIM := 1536)), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
