"""
Legacy API compatibility layer for v1 endpoints.
Provides backward compatibility with the original dashboard prototype.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.data.database.connection import get_db_connection, get_db_session
from services.data.database.models import Article, NewsSource

router = APIRouter(prefix="/api/v1", tags=["legacy-api"])


def format_legacy_response(
    data: Any, total: int = None, page: int = 1, page_size: int = 20
) -> Dict[str, Any]:
    """Format response in legacy API format."""
    response = {"status": "success", "data": data}

    if total is not None:
        response["meta"] = {"page": page, "page_size": page_size, "total": total}

    return response


def transform_article_to_legacy(article: Article) -> Dict[str, Any]:
    """Transform Article model to legacy format."""
    return {
        "id": str(article.id),
        "title": article.title,
        "summary": article.summary,
        "url": article.url,
        "date": article.published_at.strftime("%Y-%m-%d"),
        "topic": article.topic_category or "Unknown",
        "tone": article.sentiment_label or "neutral",  # sentiment_label -> tone
        "country": "Unknown",  # TODO: extract from content or add to model
        "language": "EN",  # TODO: detect language or add to model
    }


@router.get("/news")
async def get_news_legacy(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search query"),
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get paginated list of news articles."""

    # Build query
    query = select(Article).options(selectinload(Article.source))

    # Apply filters
    if topic:
        query = query.filter(Article.topic_category == topic)

    if date_from:
        start_date = datetime.fromisoformat(date_from)
        query = query.filter(Article.published_at >= start_date)

    if date_to:
        end_date = datetime.fromisoformat(date_to)
        query = query.filter(Article.published_at <= end_date)

    if search:
        search_filter = or_(
            Article.title.ilike(f"%{search}%"),
            Article.summary.ilike(f"%{search}%"),
            Article.content.ilike(f"%{search}%"),
        )
        query = query.filter(search_filter)

    # Count total items
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination and ordering
    query = query.order_by(desc(Article.published_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    # Execute query
    result = await db.execute(query)
    articles = result.scalars().all()

    # Transform to legacy format
    legacy_articles = [transform_article_to_legacy(article) for article in articles]

    return format_legacy_response(legacy_articles, total, page, page_size)


@router.get("/news/{news_id}")
async def get_news_detail_legacy(
    news_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get detailed news article."""

    try:
        article_id = int(news_id)
    except ValueError:
        return {"status": "error", "message": "Invalid article ID", "code": 400}

    query = (
        select(Article)
        .options(selectinload(Article.source))
        .filter(Article.id == article_id)
    )
    result = await db.execute(query)
    article = result.scalar_one_or_none()

    if not article:
        return {"status": "error", "message": "Article not found", "code": 404}

    legacy_article = transform_article_to_legacy(article)
    return format_legacy_response(legacy_article)


@router.get("/stats/summary")
async def get_stats_summary_legacy(
    week: Optional[int] = Query(None, description="Week number"),
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get weekly KPI summary."""

    # Calculate date range for the week
    if week:
        # For simplicity, treat week as days from start of year
        year = datetime.now().year
        start_date = datetime(year, 1, 1) + timedelta(weeks=week - 1)
        end_date = start_date + timedelta(weeks=1)
        date_filter = Article.published_at.between(start_date, end_date)
    else:
        # Last 7 days if no week specified
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        date_filter = Article.published_at.between(start_date, end_date)

    # Total articles in period
    total_query = select(func.count(Article.id)).filter(date_filter)
    total_result = await db.execute(total_query)
    total = total_result.scalar()

    # Sentiment distribution
    sentiment_query = (
        select(Article.sentiment_label, func.count())
        .filter(date_filter)
        .filter(Article.sentiment_label.isnot(None))
        .group_by(Article.sentiment_label)
    )
    sentiment_result = await db.execute(sentiment_query)
    sentiment_dist = {row[0]: row[1] for row in sentiment_result.fetchall()}

    # Countries count (simplified)
    countries = 1  # TODO: implement proper country detection

    summary = {
        "week": week or datetime.now().isocalendar()[1],
        "total": total,
        "countries": countries,
        "tones": {
            "positive": sentiment_dist.get("positive", 0),
            "neutral": sentiment_dist.get("neutral", 0),
            "negative": sentiment_dist.get("negative", 0),
        },
    }

    return format_legacy_response(summary)


@router.get("/stats/topics")
async def get_stats_topics_legacy(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    date_from: Optional[str] = Query(None, description="Start date"),
    date_to: Optional[str] = Query(None, description="End date"),
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get topic distribution."""

    query = select(Article.topic_category, func.count()).filter(
        Article.topic_category.isnot(None)
    )

    # Apply date filters
    if date_from:
        start_date = datetime.fromisoformat(date_from)
        query = query.filter(Article.published_at >= start_date)

    if date_to:
        end_date = datetime.fromisoformat(date_to)
        query = query.filter(Article.published_at <= end_date)

    query = query.group_by(Article.topic_category).order_by(desc(func.count()))

    result = await db.execute(query)
    distribution = {row[0]: row[1] for row in result.fetchall()}

    return format_legacy_response(distribution)


@router.get("/stats/tones")
async def get_stats_tones_legacy(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    date_from: Optional[str] = Query(None, description="Start date"),
    date_to: Optional[str] = Query(None, description="End date"),
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get tone distribution."""

    query = select(Article.sentiment_label, func.count()).filter(
        Article.sentiment_label.isnot(None)
    )

    # Apply date filters
    if date_from:
        start_date = datetime.fromisoformat(date_from)
        query = query.filter(Article.published_at >= start_date)

    if date_to:
        end_date = datetime.fromisoformat(date_to)
        query = query.filter(Article.published_at <= end_date)

    query = query.group_by(Article.sentiment_label)

    result = await db.execute(query)
    distribution = {row[0]: row[1] for row in result.fetchall()}

    # Transform sentiment_label to tone names for legacy compatibility
    legacy_distribution = {
        "positive": distribution.get("positive", 0),
        "neutral": distribution.get("neutral", 0),
        "negative": distribution.get("negative", 0),
    }

    return format_legacy_response(legacy_distribution)


@router.get("/stats/tones/timeline")
async def get_tones_timeline_legacy(
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    weeks: int = Query(12, ge=1, le=52, description="Number of weeks"),
    db_conn=Depends(get_db_connection),
):
    """Legacy endpoint: Get tone evolution over time."""

    cutoff_date = datetime.now(timezone.utc) - timedelta(weeks=weeks)

    query = """
    SELECT
        EXTRACT(week FROM published_at) as week_number,
        sentiment_label,
        COUNT(*) as count
    FROM articles
    WHERE published_at >= $1
        AND sentiment_label IS NOT NULL
    GROUP BY EXTRACT(week FROM published_at), sentiment_label
    ORDER BY week_number, sentiment_label
    """

    result = await db_conn.fetch(query, cutoff_date)

    # Organize data by week
    weeks_data = {}
    labels = set()

    for row in result:
        week_num = int(row["week_number"])
        sentiment = row["sentiment_label"]
        count = row["count"]

        if week_num not in weeks_data:
            weeks_data[week_num] = {}

        weeks_data[week_num][sentiment] = count
        labels.add(week_num)

    # Create time series format
    sorted_weeks = sorted(labels)
    timeline_data = {
        "labels": sorted_weeks,
        "positive": [
            weeks_data.get(week, {}).get("positive", 0) for week in sorted_weeks
        ],
        "neutral": [
            weeks_data.get(week, {}).get("neutral", 0) for week in sorted_weeks
        ],
        "negative": [
            weeks_data.get(week, {}).get("negative", 0) for week in sorted_weeks
        ],
    }

    return format_legacy_response(timeline_data)


@router.get("/stats/geo")
async def get_stats_geo_legacy(
    date_from: Optional[str] = Query(None, description="Start date"),
    date_to: Optional[str] = Query(None, description="End date"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    db_conn=Depends(get_db_connection),
):
    """Legacy endpoint: Get geographic distribution."""

    # Build base query with optional filters
    where_conditions = ["content IS NOT NULL"]
    params = []

    if date_from:
        where_conditions.append("published_at >= $" + str(len(params) + 1))
        params.append(datetime.fromisoformat(date_from))

    if date_to:
        where_conditions.append("published_at <= $" + str(len(params) + 1))
        params.append(datetime.fromisoformat(date_to))

    if topic:
        where_conditions.append("topic_category = $" + str(len(params) + 1))
        params.append(topic)

    where_clause = " AND ".join(where_conditions)

    query = f"""
    SELECT
        CASE
            WHEN content ILIKE '%united states%' OR content ILIKE '%usa%' OR content ILIKE '%america%' THEN 'US'
            WHEN content ILIKE '%canada%' THEN 'CA'
            WHEN content ILIKE '%united kingdom%' OR content ILIKE '%uk%' OR content ILIKE '%britain%' THEN 'GB'
            WHEN content ILIKE '%australia%' THEN 'AU'
            WHEN content ILIKE '%europe%' OR content ILIKE '%european%' THEN 'EU'
            WHEN content ILIKE '%global%' OR content ILIKE '%international%' OR content ILIKE '%worldwide%' THEN 'GLOBAL'
            ELSE 'OTHER'
        END as country,
        COUNT(*) as total,
        MODE() WITHIN GROUP (ORDER BY sentiment_label) as tone,
        'EN' as language
    FROM articles
    WHERE {where_clause}
    GROUP BY country
    ORDER BY total DESC
    """

    result = await db_conn.fetch(query, *params)

    geo_data = []
    for row in result:
        geo_data.append(
            {
                "country": row["country"],
                "total": row["total"],
                "tone": row["tone"] or "neutral",
                "language": row["language"],
            }
        )

    return format_legacy_response(geo_data)
