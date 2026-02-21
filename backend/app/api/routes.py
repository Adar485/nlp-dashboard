from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import json

from app.core.database import get_db
from app.core.redis import redis_client
from app.models.analysis import TextAnalysis
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, StatsResponse
from app.nlp.analyzer import analyze_text

router = APIRouter(prefix="/api", tags=["analysis"])


def extract_text_from_file(file: UploadFile) -> str:
    content = file.file.read()
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1")

    elif filename.endswith(".pdf"):
        from PyPDF2 import PdfReader
        import io
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    else:
        raise HTTPException(status_code=400, detail="Sadece .txt ve .pdf dosyaları desteklenir")


@router.post("/analyze", response_model=AnalysisResponse)
async def create_analysis(req: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    cache_key = f"analysis:{hash(req.text)}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    result = analyze_text(req.text)

    analysis = TextAnalysis(
        original_text=req.text,
        language=result["language"],
        sentiment_label=result["sentiment_label"],
        sentiment_score=result["sentiment_score"],
        entities=result["entities"],
        keywords=result["keywords"],
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    response_data = AnalysisResponse.model_validate(analysis).model_dump(mode="json")
    await redis_client.setex(cache_key, 3600, json.dumps(response_data, default=str))

    return analysis


@router.post("/analyze-file", response_model=AnalysisResponse)
async def analyze_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    text = extract_text_from_file(file)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Dosyadan metin çıkarılamadı")

    result = analyze_text(text)

    analysis = TextAnalysis(
        original_text=text[:5000],
        language=result["language"],
        sentiment_label=result["sentiment_label"],
        sentiment_score=result["sentiment_score"],
        entities=result["entities"],
        keywords=result["keywords"],
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    return analysis


@router.get("/analyses", response_model=list[AnalysisResponse])
async def get_analyses(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TextAnalysis).order_by(TextAnalysis.created_at.desc()).limit(limit)
    )
    return result.scalars().all()


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    total = await db.execute(select(func.count(TextAnalysis.id)))
    total_count = total.scalar() or 0

    dist_query = await db.execute(
        select(TextAnalysis.sentiment_label, func.count(TextAnalysis.id))
        .group_by(TextAnalysis.sentiment_label)
    )
    distribution = {row[0]: row[1] for row in dist_query.all()}

    avg = await db.execute(select(func.avg(TextAnalysis.sentiment_score)))
    avg_score = round(float(avg.scalar() or 0), 4)

    return StatsResponse(
        total_analyses=total_count,
        sentiment_distribution=distribution,
        avg_sentiment_score=avg_score,
    )