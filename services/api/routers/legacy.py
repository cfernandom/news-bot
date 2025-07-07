"""
Legacy API compatibility layer for v1 endpoints.
Provides backward compatibility with the original dashboard prototype.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
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
    # Map source URL to country
    country_mapping = {
        "breastcancer.org": "US",
        "webmd.com": "US",
        "curetoday.com": "US",
        "news-medical.net": "UK",
        "breastcancernow.org": "UK",
        "medicalxpress.com": "DE",
        "nature.com": "UK",
        "sciencedaily.com": "US",
    }

    # Extract country from source URL
    source_country = "Unknown"
    if article.source and article.source.base_url:
        for domain, country in country_mapping.items():
            if domain in article.source.base_url:
                source_country = country
                break

    return {
        "id": str(article.id),
        "title": article.title,
        "summary": article.summary,
        "url": article.url,
        "date": article.published_at.strftime("%Y-%m-%d"),
        "topic": article.topic_category or "Unknown",
        "tone": article.sentiment_label or "neutral",  # sentiment_label -> tone
        "country": source_country,  # Real country from source mapping
        "language": article.language or "en",  # Real language from database
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
        try:
            start_date = datetime.fromisoformat(date_from)
            query = query.filter(Article.published_at >= start_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format for date_from: {date_from}. Use YYYY-MM-DD format.",
            )

    if date_to:
        try:
            end_date = datetime.fromisoformat(date_to)
            query = query.filter(Article.published_at <= end_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format for date_to: {date_to}. Use YYYY-MM-DD format.",
            )

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

    # Countries count based on actual article data
    countries_query = (
        select(func.count(func.distinct(Article.country)))
        .filter(date_filter)
        .filter(Article.country.isnot(None))
    )
    countries_result = await db.execute(countries_query)
    countries = countries_result.scalar() or 0

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

    cutoff_date = datetime.now() - timedelta(weeks=weeks)

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
    """Legacy endpoint: Get geographic distribution by country as per endpoints.md."""

    # Build filters for the SQL query
    where_conditions = ["a.sentiment_label IS NOT NULL"]
    params = []

    if date_from:
        where_conditions.append("a.published_at >= $" + str(len(params) + 1))
        params.append(datetime.fromisoformat(date_from))

    if date_to:
        where_conditions.append("a.published_at <= $" + str(len(params) + 1))
        params.append(datetime.fromisoformat(date_to))

    if topic:
        where_conditions.append("a.topic_category = $" + str(len(params) + 1))
        params.append(topic)

    where_clause = " AND ".join(where_conditions)

    # Use raw SQL as it works perfectly in PostgreSQL
    query = f"""
    SELECT
        CASE
            WHEN ns.base_url ILIKE '%breastcancer.org%' THEN 'US'
            WHEN ns.base_url ILIKE '%curetoday.com%' THEN 'US'
            WHEN ns.base_url ILIKE '%webmd.com%' THEN 'US'
            WHEN ns.base_url ILIKE '%news-medical.net%' THEN 'UK'
            ELSE 'Other'
        END as country,
        a.sentiment_label as tone,
        COUNT(*) as total
    FROM articles a
    LEFT JOIN news_sources ns ON a.source_id = ns.id
    WHERE {where_clause}
    GROUP BY
        CASE
            WHEN ns.base_url ILIKE '%breastcancer.org%' THEN 'US'
            WHEN ns.base_url ILIKE '%curetoday.com%' THEN 'US'
            WHEN ns.base_url ILIKE '%webmd.com%' THEN 'US'
            WHEN ns.base_url ILIKE '%news-medical.net%' THEN 'UK'
            ELSE 'Other'
        END,
        a.sentiment_label
    ORDER BY total DESC
    """

    result = await db_conn.fetch(query, *params)

    # Transform to expected format as per endpoints.md
    geo_data = []
    for row in result:
        geo_data.append(
            {
                "country": row["country"],
                "total": row["total"],
                "tone": row["tone"] or "neutral",
                "language": "EN",
            }
        )

    return format_legacy_response(geo_data)


@router.get("/analytics/language-distribution")
async def get_language_distribution_legacy(
    date_from: Optional[str] = Query(None, description="Start date"),
    date_to: Optional[str] = Query(None, description="End date"),
    db: AsyncSession = Depends(get_db_session),
):
    """Legacy endpoint: Get language distribution from articles."""

    # Query language distribution from articles table
    query = select(Article.language, func.count()).filter(Article.language.isnot(None))

    # Apply date filters
    if date_from:
        start_date = datetime.fromisoformat(date_from)
        query = query.filter(Article.published_at >= start_date)

    if date_to:
        end_date = datetime.fromisoformat(date_to)
        query = query.filter(Article.published_at <= end_date)

    query = query.group_by(Article.language).order_by(desc(func.count()))

    result = await db.execute(query)
    raw_distribution = {row[0]: row[1] for row in result.fetchall()}

    # Transform language codes to expected format
    distribution = []
    for lang_code, count in raw_distribution.items():
        if lang_code and count > 0:
            # Map language codes to expected format
            if lang_code.lower() in ["en", "english"]:
                sentiment_label = "english"
            elif lang_code.lower() in ["es", "spanish", "español"]:
                sentiment_label = "spanish"
            else:
                sentiment_label = "other"

            distribution.append({"sentiment_label": sentiment_label, "count": count})

    return format_legacy_response(distribution)


@router.get("/stats/articles/daily")
async def get_articles_daily_timeline_legacy(
    days: int = Query(7, ge=1, le=30, description="Number of days"),
    db_conn=Depends(get_db_connection),
):
    """Legacy endpoint: Get daily articles count over time."""

    cutoff_date = datetime.now() - timedelta(days=days)

    query = """
    SELECT
        DATE(published_at) as day,
        COUNT(*) as count
    FROM articles
    WHERE published_at >= $1
    GROUP BY DATE(published_at)
    ORDER BY day
    """

    result = await db_conn.fetch(query, cutoff_date)

    # Format for LegacyTrendChart
    daily_data = []
    for row in result:
        daily_data.append(
            {"day": row["day"].strftime("%Y-%m-%d"), "count": row["count"]}
        )

    return format_legacy_response(daily_data)


@router.get("/stats/topics/language-breakdown")
async def get_topics_language_breakdown_legacy(
    weeks: int = Query(8, ge=1, le=52, description="Number of weeks"),
    db_conn=Depends(get_db_connection),
):
    """Legacy endpoint: Get topics distribution with language breakdown."""

    # Use a broader date range since our data spans multiple weeks
    cutoff_date = datetime.now() - timedelta(weeks=weeks)

    query = """
    SELECT
        a.topic_category,
        a.language,
        COUNT(*) as count
    FROM articles a
    WHERE a.published_at >= $1
        AND a.topic_category IS NOT NULL
        AND a.language IS NOT NULL
    GROUP BY a.topic_category, a.language
    ORDER BY a.topic_category, a.language
    """

    result = await db_conn.fetch(query, cutoff_date)

    # Organize data by topic with language breakdown
    topics_data = {}
    for row in result:
        topic = row["topic_category"]
        language = row["language"]
        count = row["count"]

        if topic not in topics_data:
            topics_data[topic] = {
                "topic_category": topic,
                "english": 0,
                "spanish": 0,
                "total": 0,
            }

        # Map language codes to expected format
        if language and language.upper() == "EN":
            topics_data[topic]["english"] = count
        elif language and language.upper() == "ES":
            topics_data[topic]["spanish"] = count

        topics_data[topic]["total"] += count

    # Convert to list and sort by total
    topics_list = list(topics_data.values())
    topics_list.sort(key=lambda x: x["total"], reverse=True)

    return format_legacy_response(topics_list)
