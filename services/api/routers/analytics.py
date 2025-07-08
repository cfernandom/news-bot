"""
Analytics API endpoints for dashboard metrics and trend analysis.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.data.database.connection import get_db_connection, get_db_session
from services.data.database.models import Article, DashboardSummary, NewsSource

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(
    days: int = Query(30, ge=1, le=365, description="Analysis period in days"),
    db: AsyncSession = Depends(get_db_session),
):
    """Get comprehensive dashboard summary with key metrics."""

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Total articles
    total_query = select(func.count(Article.id))
    total_result = await db.execute(total_query)
    total_articles = total_result.scalar()

    # Recent articles in specified period
    recent_query = select(func.count(Article.id)).filter(
        Article.published_at >= cutoff_date
    )
    recent_result = await db.execute(recent_query)
    recent_articles = recent_result.scalar()

    # Sentiment distribution (all time)
    sentiment_query = (
        select(Article.sentiment_label, func.count())
        .filter(Article.sentiment_label.isnot(None))
        .group_by(Article.sentiment_label)
    )
    sentiment_result = await db.execute(sentiment_query)
    sentiment_dist = {row[0]: row[1] for row in sentiment_result.fetchall()}

    # Topic distribution (all time)
    topic_query = (
        select(Article.topic_category, func.count())
        .filter(Article.topic_category.isnot(None))
        .group_by(Article.topic_category)
    )
    topic_result = await db.execute(topic_query)
    topic_dist = {row[0]: row[1] for row in topic_result.fetchall()}

    # Active sources
    sources_query = select(func.count(func.distinct(Article.source_id)))
    sources_result = await db.execute(sources_query)
    active_sources = sources_result.scalar()

    # Average sentiment score
    avg_sentiment_query = select(func.avg(Article.sentiment_score)).filter(
        Article.sentiment_score.isnot(None)
    )
    avg_sentiment_result = await db.execute(avg_sentiment_query)
    avg_sentiment = float(avg_sentiment_result.scalar() or 0.0)

    return DashboardSummary(
        total_articles=total_articles,
        recent_articles=recent_articles,
        sentiment_distribution=sentiment_dist,
        topic_distribution=topic_dist,
        active_sources=active_sources,
        avg_sentiment_score=round(avg_sentiment, 3),
        analysis_period_days=days,
    )


@router.get("/sentiment/trends")
async def get_sentiment_trends(
    days: int = Query(30, ge=7, le=365, description="Analysis period in days"),
    db_conn=Depends(get_db_connection),
):
    """Get sentiment trends over time."""

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    # Daily sentiment aggregation
    query = """
    SELECT
        DATE(published_at) as date,
        sentiment_label,
        COUNT(*) as count,
        AVG(sentiment_score) as avg_score
    FROM articles
    WHERE published_at >= $1
        AND sentiment_label IS NOT NULL
        AND sentiment_score IS NOT NULL
    GROUP BY DATE(published_at), sentiment_label
    ORDER BY date DESC, sentiment_label
    """

    result = await db_conn.fetch(query, cutoff_date)

    # Group by date
    trends = {}
    for row in result:
        date_str = row["date"].isoformat()
        if date_str not in trends:
            trends[date_str] = {}

        trends[date_str][row["sentiment_label"]] = {
            "count": row["count"],
            "avg_score": float(row["avg_score"]),
        }

    return {"trends": trends, "period_days": days, "total_data_points": len(result)}


@router.get("/topics/distribution")
async def get_topic_distribution(
    days: Optional[int] = Query(
        None, ge=1, le=365, description="Filter by last N days"
    ),
    db: AsyncSession = Depends(get_db_session),
):
    """Get topic distribution with optional time filtering."""

    query = select(Article.topic_category, func.count()).filter(
        Article.topic_category.isnot(None)
    )

    if days:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.filter(Article.published_at >= cutoff_date)

    query = query.group_by(Article.topic_category).order_by(desc(func.count()))

    result = await db.execute(query)
    distribution = {row[0]: row[1] for row in result.fetchall()}

    return {
        "distribution": distribution,
        "total_articles": sum(distribution.values()),
        "unique_topics": len(distribution),
        "period_days": days or "all_time",
    }


@router.get("/sources/performance")
async def get_sources_performance(db_conn=Depends(get_db_connection)):
    """Get performance metrics by news source."""

    query = """
    SELECT
        ns.name as source_name,
        ns.url as source_url,
        COUNT(a.id) as total_articles,
        COUNT(CASE WHEN a.sentiment_label IS NOT NULL THEN 1 END) as analyzed_articles,
        AVG(a.sentiment_score) as avg_sentiment,
        MODE() WITHIN GROUP (ORDER BY a.sentiment_label) as dominant_sentiment,
        MAX(a.published_at) as latest_article,
        MIN(a.published_at) as earliest_article
    FROM news_sources ns
    LEFT JOIN articles a ON ns.id = a.source_id
    GROUP BY ns.id, ns.name, ns.url
    HAVING COUNT(a.id) > 0
    ORDER BY total_articles DESC
    """

    result = await db_conn.fetch(query)

    sources = []
    for row in result:
        sources.append(
            {
                "source_name": row["source_name"],
                "source_url": row["source_url"],
                "total_articles": row["total_articles"],
                "analyzed_articles": row["analyzed_articles"],
                "analysis_coverage": (
                    round((row["analyzed_articles"] / row["total_articles"]) * 100, 1)
                    if row["total_articles"] > 0
                    else 0
                ),
                "avg_sentiment": (
                    round(float(row["avg_sentiment"]), 3)
                    if row["avg_sentiment"]
                    else None
                ),
                "dominant_sentiment": row["dominant_sentiment"],
                "latest_article": (
                    row["latest_article"].isoformat() if row["latest_article"] else None
                ),
                "earliest_article": (
                    row["earliest_article"].isoformat()
                    if row["earliest_article"]
                    else None
                ),
            }
        )

    return {"sources": sources, "total_sources": len(sources)}


@router.get("/geographic/distribution")
async def get_geographic_distribution(db_conn=Depends(get_db_connection)):
    """Get geographic distribution of news articles."""

    # Extract country/region information from content or metadata
    query = """
    SELECT
        CASE
            WHEN content ILIKE '%united states%' OR content ILIKE '%usa%' OR content ILIKE '%america%' THEN 'United States'
            WHEN content ILIKE '%canada%' THEN 'Canada'
            WHEN content ILIKE '%united kingdom%' OR content ILIKE '%uk%' OR content ILIKE '%britain%' THEN 'United Kingdom'
            WHEN content ILIKE '%australia%' THEN 'Australia'
            WHEN content ILIKE '%europe%' OR content ILIKE '%european%' THEN 'Europe'
            WHEN content ILIKE '%global%' OR content ILIKE '%international%' OR content ILIKE '%worldwide%' THEN 'Global'
            ELSE 'Other/Unknown'
        END as region,
        COUNT(*) as article_count,
        AVG(sentiment_score) as avg_sentiment
    FROM articles
    WHERE content IS NOT NULL
    GROUP BY
        CASE
            WHEN content ILIKE '%united states%' OR content ILIKE '%usa%' OR content ILIKE '%america%' THEN 'United States'
            WHEN content ILIKE '%canada%' THEN 'Canada'
            WHEN content ILIKE '%united kingdom%' OR content ILIKE '%uk%' OR content ILIKE '%britain%' THEN 'United Kingdom'
            WHEN content ILIKE '%australia%' THEN 'Australia'
            WHEN content ILIKE '%europe%' OR content ILIKE '%european%' THEN 'Europe'
            WHEN content ILIKE '%global%' OR content ILIKE '%international%' OR content ILIKE '%worldwide%' THEN 'Global'
            ELSE 'Other/Unknown'
        END
    ORDER BY article_count DESC
    """

    result = await db_conn.fetch(query)

    distribution = {}
    for row in result:
        distribution[row["region"]] = {
            "article_count": row["article_count"],
            "avg_sentiment": (
                round(float(row["avg_sentiment"]), 3) if row["avg_sentiment"] else None
            ),
        }

    return {
        "distribution": distribution,
        "total_articles": sum(item["article_count"] for item in distribution.values()),
        "note": "Geographic classification based on content analysis keywords",
    }


@router.get("/trends/weekly")
async def get_weekly_trends(
    weeks: int = Query(12, ge=1, le=52, description="Number of weeks to analyze"),
    db_conn=Depends(get_db_connection),
):
    """Get weekly publication and sentiment trends."""

    cutoff_date = datetime.now(timezone.utc) - timedelta(weeks=weeks)

    query = """
    SELECT
        DATE_TRUNC('week', published_at) as week_start,
        COUNT(*) as article_count,
        COUNT(CASE WHEN sentiment_label = 'positive' THEN 1 END) as positive_count,
        COUNT(CASE WHEN sentiment_label = 'negative' THEN 1 END) as negative_count,
        COUNT(CASE WHEN sentiment_label = 'neutral' THEN 1 END) as neutral_count,
        AVG(sentiment_score) as avg_sentiment_score
    FROM articles
    WHERE published_at >= $1
    GROUP BY DATE_TRUNC('week', published_at)
    ORDER BY week_start DESC
    """

    result = await db_conn.fetch(query)

    trends = []
    for row in result:
        trends.append(
            {
                "week_start": row["week_start"].isoformat(),
                "article_count": row["article_count"],
                "sentiment_counts": {
                    "positive": row["positive_count"],
                    "negative": row["negative_count"],
                    "neutral": row["neutral_count"],
                },
                "avg_sentiment_score": (
                    round(float(row["avg_sentiment_score"]), 3)
                    if row["avg_sentiment_score"]
                    else None
                ),
            }
        )

    return {"weekly_trends": trends, "period_weeks": weeks, "total_weeks": len(trends)}
