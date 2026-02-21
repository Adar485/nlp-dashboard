from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class TextAnalysis(Base):
    __tablename__ = "text_analyses"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    language = Column(String(10))
    sentiment_label = Column(String(20))
    sentiment_score = Column(Float)
    entities = Column(JSON)
    keywords = Column(JSON)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())