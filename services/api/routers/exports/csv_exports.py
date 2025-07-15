"""
CSV export functionality.
Handles CSV file generation and download endpoints.
"""

import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import get_db_session

from .shared import get_filtered_articles, track_export

router = APIRouter()


@router.get("/news.csv")
async def export_news_csv(
    response: Response,
    db: AsyncSession = Depends(get_db_session),
    search: Optional[str] = Query(None, description="Search term for filtering"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    source_id: Optional[int] = Query(None, description="Filter by source ID"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    min_word_count: Optional[int] = Query(None, description="Minimum word count"),
    max_word_count: Optional[int] = Query(None, description="Maximum word count"),
    limit: int = Query(1000, description="Maximum number of records"),
):
    """
    Export news articles to CSV format.

    Returns a CSV file with filtered articles based on the provided parameters.
    Includes comprehensive metadata for each article.
    """
    # Get filtered articles
    articles = await get_filtered_articles(
        db,
        search,
        start_date,
        end_date,
        source_id,
        sentiment,
        country,
        language,
        min_word_count,
        max_word_count,
        limit,
    )

    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(
        [
            "ID",
            "Title",
            "URL",
            "Source",
            "Published Date",
            "Scraped Date",
            "Summary",
            "Language",
            "Country",
            "Word Count",
            "Sentiment Score",
            "Processing Status",
            "Content Hash",
        ]
    )

    # Write data rows
    for article in articles:
        writer.writerow(
            [
                article.id,
                article.title,
                article.url,
                article.source.name if article.source else "Unknown",
                article.published_at.isoformat() if article.published_at else "",
                article.scraped_at.isoformat() if article.scraped_at else "",
                article.summary or "",
                article.language or "",
                article.country or "",
                article.word_count or 0,
                article.sentiment_score or "",
                article.processing_status or "",
                article.content_hash or "",
            ]
        )

    # Track export
    filename = f"news_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_content = output.getvalue()
    track_export("CSV", filename, file_size=len(csv_content.encode("utf-8")))

    # Set response headers
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"

    return Response(content=csv_content, media_type="text/csv")
