"""
NLP API endpoints for sentiment analysis and topic classification.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import get_db_session
from services.data.database.models import Article
from services.nlp.src.sentiment import get_sentiment_analyzer
from services.nlp.src.topic_classifier import get_topic_classifier

router = APIRouter(prefix="/nlp", tags=["nlp"])


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""

    text: str = Field(..., description="Text to analyze", max_length=10000)
    title: str = Field(None, description="Optional title for context", max_length=500)


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""

    sentiment_label: str = Field(..., description="Sentiment classification")
    confidence: float = Field(..., description="Confidence score (0-1)")
    scores: Dict[str, float] = Field(..., description="Raw sentiment scores")
    compound_score: float = Field(..., description="VADER compound score")


class TopicRequest(BaseModel):
    """Request model for topic classification."""

    title: str = Field(..., description="Article title", max_length=500)
    summary: str = Field(None, description="Article summary", max_length=2000)
    content: str = Field(None, description="Article content", max_length=10000)


class TopicResponse(BaseModel):
    """Response model for topic classification."""

    topic_category: str = Field(..., description="Classified topic category")
    confidence: float = Field(..., description="Classification confidence")
    matched_keywords: List[str] = Field(
        ..., description="Keywords that influenced classification"
    )


class BatchSentimentResponse(BaseModel):
    """Response model for batch sentiment analysis."""

    processed_count: int = Field(..., description="Number of articles processed")
    updated_count: int = Field(..., description="Number of articles updated")
    errors: List[str] = Field(default_factory=list, description="Processing errors")


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment for a given text."""

    try:
        analyzer = get_sentiment_analyzer()
        result = analyzer.analyze_sentiment(text=request.text, title=request.title)

        return SentimentResponse(
            sentiment_label=result["sentiment_label"],
            confidence=result["confidence"],
            scores=result["scores"],
            compound_score=result["scores"]["compound"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Sentiment analysis failed: {str(e)}"
        )


@router.post("/topic", response_model=TopicResponse)
async def classify_topic(request: TopicRequest):
    """Classify topic for article content."""

    try:
        classifier = get_topic_classifier()

        # Create a temporary article-like object for classification
        article_data = {
            "title": request.title,
            "summary": request.summary or "",
            "content": request.content or "",
        }

        result = classifier.classify_article(article_data)

        return TopicResponse(
            topic_category=result["topic_category"],
            confidence=result["confidence"],
            matched_keywords=result["matched_keywords"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Topic classification failed: {str(e)}"
        )


@router.post("/batch-sentiment", response_model=BatchSentimentResponse)
async def batch_sentiment_analysis(
    limit: int = 50,
    skip_analyzed: bool = True,
    db: AsyncSession = Depends(get_db_session),
):
    """Perform batch sentiment analysis on articles."""

    try:
        from sqlalchemy import select, update

        # Build query for articles needing analysis
        query = select(Article)

        if skip_analyzed:
            query = query.filter(Article.sentiment_label.is_(None))

        query = query.limit(limit)

        result = await db.execute(query)
        articles = result.scalars().all()

        if not articles:
            return BatchSentimentResponse(
                processed_count=0,
                updated_count=0,
                errors=["No articles found for processing"],
            )

        # Initialize sentiment analyzer
        analyzer = get_sentiment_analyzer()

        processed_count = 0
        updated_count = 0
        errors = []

        for article in articles:
            try:
                # Analyze sentiment
                sentiment_result = analyzer.analyze_sentiment(
                    text=article.summary or article.content or "", title=article.title
                )

                # Update article with sentiment data
                article.sentiment_label = sentiment_result["sentiment_label"]
                article.sentiment_score = sentiment_result["scores"]["compound"]
                article.sentiment_data = sentiment_result["scores"]

                processed_count += 1

            except Exception as e:
                errors.append(f"Article {article.id}: {str(e)}")
                processed_count += 1
                continue

        # Commit changes
        await db.commit()
        updated_count = processed_count - len(errors)

        return BatchSentimentResponse(
            processed_count=processed_count, updated_count=updated_count, errors=errors
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Batch processing failed: {str(e)}"
        )


@router.get("/analyzers/status")
async def get_analyzers_status():
    """Get status and information about NLP analyzers."""

    try:
        # Test sentiment analyzer
        sentiment_analyzer = get_sentiment_analyzer()
        sentiment_test = sentiment_analyzer.analyze_sentiment(
            "This is a test sentence for sentiment analysis."
        )

        # Test topic classifier
        topic_classifier = get_topic_classifier()
        topic_test = topic_classifier.classify_article(
            {
                "title": "Breast Cancer Research Update",
                "summary": "New research shows promising results",
                "content": "Scientists have discovered new treatment options",
            }
        )

        return {
            "sentiment_analyzer": {
                "status": "operational",
                "test_result": sentiment_test["sentiment_label"],
                "model_info": "VADER + spaCy medical specialization",
            },
            "topic_classifier": {
                "status": "operational",
                "test_result": topic_test["topic_category"],
                "available_topics": topic_classifier.get_available_topics(),
            },
            "system_status": "all_systems_operational",
        }

    except Exception as e:
        return {
            "sentiment_analyzer": {"status": "error", "error": str(e)},
            "topic_classifier": {"status": "error", "error": str(e)},
            "system_status": "degraded",
        }


@router.get("/models/info")
async def get_models_info():
    """Get detailed information about NLP models and capabilities."""

    return {
        "sentiment_analysis": {
            "model": "VADER (Valence Aware Dictionary and sEntiment Reasoner)",
            "preprocessing": "spaCy 3.8.7 with en_core_web_sm",
            "specialization": "Medical content with conservative thresholds",
            "thresholds": {
                "positive": ">= 0.3 (vs 0.05 standard)",
                "negative": "<= -0.3 (vs -0.05 standard)",
                "neutral": "-0.3 to 0.3",
            },
            "performance": "~2 articles/second batch processing",
        },
        "topic_classification": {
            "model": "Rule-based medical topic classifier",
            "categories": [
                "Treatment",
                "Prevention",
                "Research",
                "Diagnosis",
                "Surgery",
                "Chemotherapy",
                "Radiation",
                "Immunotherapy",
                "Clinical Trials",
                "General",
            ],
            "method": "Keyword matching with medical terminology",
            "confidence": "Based on keyword relevance scoring",
        },
        "system_info": {
            "version": "1.0.0",
            "last_updated": "2025-06-30",
            "total_categories": 10,
            "supported_languages": ["English"],
        },
    }
