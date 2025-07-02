"""
Articles API endpoints for CRUD operations and search.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.data.database.connection import get_db_session
from services.data.database.models import (
    Article,
    ArticleCreate,
    ArticleResponse,
    ArticleUpdate,
    NewsSource,
    PaginatedResponse,
)

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=PaginatedResponse[ArticleResponse])
async def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=200, description="Items per page"),
    source: Optional[str] = Query(None, description="Filter by news source"),
    sentiment: Optional[str] = Query(
        None, description="Filter by sentiment (positive/negative/neutral)"
    ),
    topic: Optional[str] = Query(None, description="Filter by topic category"),
    days: Optional[int] = Query(None, ge=1, description="Articles from last N days"),
    db: AsyncSession = Depends(get_db_session),
):
    """Get paginated list of articles with filtering options."""

    # Build query with filters
    query = select(Article).options(selectinload(Article.source))

    # Apply filters
    if source:
        query = query.join(NewsSource).filter(NewsSource.name.ilike(f"%{source}%"))

    if sentiment:
        query = query.filter(Article.sentiment_label == sentiment)

    if topic:
        query = query.filter(Article.topic_category == topic)

    if days:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.filter(Article.published_at >= cutoff_date)

    # Count total items
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination and ordering
    query = query.order_by(desc(Article.published_at))
    query = query.offset((page - 1) * size).limit(size)

    # Execute query
    result = await db.execute(query)
    articles = result.scalars().all()

    # Convert to response models
    items = [ArticleResponse.model_validate(article) for article in articles]

    return PaginatedResponse(
        items=items, total=total, page=page, size=size, pages=(total + size - 1) // size
    )


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db_session)):
    """Get a single article by ID."""

    query = (
        select(Article)
        .options(selectinload(Article.source))
        .filter(Article.id == article_id)
    )
    result = await db.execute(query)
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return ArticleResponse.model_validate(article)


@router.get("/search/", response_model=PaginatedResponse[ArticleResponse])
async def search_articles(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=200, description="Items per page"),
    db: AsyncSession = Depends(get_db_session),
):
    """Search articles by title, summary, or content."""

    # Search in title, summary, and content fields
    search_filter = or_(
        Article.title.ilike(f"%{q}%"),
        Article.summary.ilike(f"%{q}%"),
        Article.content.ilike(f"%{q}%"),
    )

    # Build query
    query = select(Article).options(selectinload(Article.source)).filter(search_filter)

    # Count total results
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination and ordering by relevance (newest first)
    query = query.order_by(desc(Article.published_at))
    query = query.offset((page - 1) * size).limit(size)

    # Execute query
    result = await db.execute(query)
    articles = result.scalars().all()

    # Convert to response models
    items = [ArticleResponse.model_validate(article) for article in articles]

    return PaginatedResponse(
        items=items, total=total, page=page, size=size, pages=(total + size - 1) // size
    )


@router.get("/stats/summary")
async def get_articles_summary(db: AsyncSession = Depends(get_db_session)):
    """Get summary statistics for articles."""

    # Total articles
    total_query = select(func.count(Article.id))
    total_result = await db.execute(total_query)
    total_articles = total_result.scalar()

    # Articles by sentiment
    sentiment_query = (
        select(Article.sentiment_label, func.count())
        .filter(Article.sentiment_label.isnot(None))
        .group_by(Article.sentiment_label)
    )
    sentiment_result = await db.execute(sentiment_query)
    sentiment_distribution = {row[0]: row[1] for row in sentiment_result.fetchall()}

    # Articles by topic
    topic_query = (
        select(Article.topic_category, func.count())
        .filter(Article.topic_category.isnot(None))
        .group_by(Article.topic_category)
    )
    topic_result = await db.execute(topic_query)
    topic_distribution = {row[0]: row[1] for row in topic_result.fetchall()}

    # Recent articles (last 7 days)
    recent_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    recent_query = select(func.count(Article.id)).filter(
        Article.published_at >= recent_cutoff
    )
    recent_result = await db.execute(recent_query)
    recent_articles = recent_result.scalar()

    return {
        "total_articles": total_articles,
        "recent_articles": recent_articles,
        "sentiment_distribution": sentiment_distribution,
        "topic_distribution": topic_distribution,
        "articles_with_sentiment": sum(sentiment_distribution.values()),
        "articles_with_topics": sum(topic_distribution.values()),
    }
