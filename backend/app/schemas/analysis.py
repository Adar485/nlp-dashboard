from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnalysisRequest(BaseModel):
    text: str


class AnalysisResponse(BaseModel):
    id: int
    original_text: str
    language: Optional[str]
    sentiment_label: str
    sentiment_score: float
    entities: list
    keywords: list
    created_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_analyses: int
    sentiment_distribution: dict
    avg_sentiment_score: float