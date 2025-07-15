"""
Excel export functionality.
Handles XLSX file generation and download endpoints.
"""

import io
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import get_db_session

from .shared import get_filtered_articles, track_export

router = APIRouter()


@router.get("/news.xlsx")
async def export_news_xlsx(
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
    Export news articles to Excel format.

    Returns an XLSX file with filtered articles, including metadata and charts.
    Provides a comprehensive spreadsheet with multiple sheets for different views.
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

    # Prepare data for Excel
    data = []
    for article in articles:
        data.append(
            {
                "ID": article.id,
                "Title": article.title,
                "URL": article.url,
                "Source": article.source.name if article.source else "Unknown",
                "Published Date": article.published_at,
                "Scraped Date": article.scraped_at,
                "Summary": article.summary or "",
                "Language": article.language or "",
                "Country": article.country or "",
                "Word Count": article.word_count or 0,
                "Sentiment Score": article.sentiment_score or "",
                "Processing Status": article.processing_status or "",
                "Content Hash": article.content_hash or "",
            }
        )

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create Excel file in memory
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Main data sheet
        df.to_excel(writer, sheet_name="Articles", index=False)

        # Summary sheet
        if not df.empty:
            summary_data = {
                "Metric": [
                    "Total Articles",
                    "Date Range",
                    "Languages",
                    "Countries",
                    "Sources",
                    "Avg Word Count",
                    "Export Date",
                ],
                "Value": [
                    len(df),
                    (
                        f"{df['Published Date'].min()} to {df['Published Date'].max()}"
                        if not df.empty
                        else "N/A"
                    ),
                    df["Language"].nunique(),
                    df["Country"].nunique(),
                    df["Source"].nunique(),
                    df["Word Count"].mean() if "Word Count" in df.columns else 0,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ],
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

    # Track export
    filename = f"news_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    excel_content = output.getvalue()
    track_export("Excel", filename, file_size=len(excel_content))

    # Set response headers
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
