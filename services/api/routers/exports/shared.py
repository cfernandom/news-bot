"""
Shared utilities for export functionality.
Common functions and utilities used across export modules.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.data.database.models import Article

# In-memory export tracking (for demonstration - in production use database)
export_history = []


def track_export(
    export_type: str, filename: str, user_id: str = "anonymous", file_size: int = 0
):
    """Track export operation for history."""
    export_record = {
        "id": len(export_history) + 1,
        "type": export_type,
        "filename": filename,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "file_size": file_size,
        "status": "completed",
    }
    export_history.append(export_record)

    # Keep only last 100 exports to prevent memory issues
    if len(export_history) > 100:
        export_history.pop(0)

    return export_record


async def get_filtered_articles(
    db: AsyncSession,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    source_id: Optional[int] = None,
    sentiment: Optional[str] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    min_word_count: Optional[int] = None,
    max_word_count: Optional[int] = None,
    limit: int = 1000,
) -> list[Article]:
    """
    Get filtered articles for export.

    Args:
        db: Database session
        search: Text search filter
        start_date: Start date filter
        end_date: End date filter
        source_id: Source ID filter
        sentiment: Sentiment filter
        country: Country filter
        language: Language filter
        min_word_count: Minimum word count filter
        max_word_count: Maximum word count filter
        limit: Maximum number of articles to return

    Returns:
        List of filtered articles
    """
    query = select(Article).options(selectinload(Article.source))

    # Apply filters
    if search:
        query = query.filter(
            or_(
                Article.title.ilike(f"%{search}%"),
                Article.summary.ilike(f"%{search}%"),
                Article.content.ilike(f"%{search}%"),
            )
        )

    if start_date:
        query = query.filter(Article.published_at >= start_date)

    if end_date:
        query = query.filter(Article.published_at <= end_date)

    if source_id:
        query = query.filter(Article.source_id == source_id)

    if sentiment:
        query = query.filter(Article.sentiment_score.ilike(f"%{sentiment}%"))

    if country:
        query = query.filter(Article.country == country)

    if language:
        query = query.filter(Article.language == language)

    if min_word_count:
        query = query.filter(Article.word_count >= min_word_count)

    if max_word_count:
        query = query.filter(Article.word_count <= max_word_count)

    # Order by published date (newest first) and limit
    query = query.order_by(desc(Article.published_at)).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()
