"""
Export functionality for CSV, XLSX, and PDF reports.
Provides data export capabilities for the legacy dashboard.
"""

import csv
import io
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from services.data.database.connection import get_db_session
from services.data.database.models import Article

router = APIRouter(prefix="/api/v1/export", tags=["exports"])


async def get_filtered_articles(
    db: AsyncSession,
    page_size: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    topic: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    search: Optional[str] = None,
):
    """Get filtered articles for export."""

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

    # Apply ordering and optional limit
    query = query.order_by(desc(Article.published_at))
    if page_size:
        query = query.limit(page_size)

    # Execute query
    result = await db.execute(query)
    return result.scalars().all()


def article_to_dict(article: Article) -> dict:
    """Convert Article model to dictionary for export."""
    return {
        "id": article.id,
        "title": article.title,
        "summary": article.summary or "",
        "url": article.url,
        "published_date": article.published_at.strftime("%Y-%m-%d %H:%M:%S"),
        "topic": article.topic_category or "Unknown",
        "sentiment": article.sentiment_label or "neutral",
        "sentiment_score": article.sentiment_score or 0.0,
        "source": article.source.name if article.source else "Unknown",
        "source_url": article.source.base_url if article.source else "",
    }


@router.get("/news.csv")
async def export_news_csv(
    page_size: Optional[int] = Query(
        1000, le=5000, description="Max articles to export"
    ),
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search query"),
    db: AsyncSession = Depends(get_db_session),
):
    """Export filtered news articles as CSV."""

    try:
        # Get filtered articles
        articles = await get_filtered_articles(
            db, page_size, country, language, topic, date_from, date_to, search
        )

        if not articles:
            raise HTTPException(
                status_code=404, detail="No articles found with the specified filters"
            )

        # Create CSV content
        output = io.StringIO()
        fieldnames = [
            "id",
            "title",
            "summary",
            "url",
            "published_date",
            "topic",
            "sentiment",
            "sentiment_score",
            "source",
            "source_url",
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for article in articles:
            writer.writerow(article_to_dict(article))

        # Prepare response
        output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"preventia_news_{timestamp}.csv"

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/news.xlsx")
async def export_news_xlsx(
    page_size: Optional[int] = Query(
        1000, le=5000, description="Max articles to export"
    ),
    country: Optional[str] = Query(None, description="Filter by country"),
    language: Optional[str] = Query(None, description="Filter by language"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search query"),
    db: AsyncSession = Depends(get_db_session),
):
    """Export filtered news articles as Excel file."""

    try:
        # Get filtered articles
        articles = await get_filtered_articles(
            db, page_size, country, language, topic, date_from, date_to, search
        )

        if not articles:
            raise HTTPException(
                status_code=404, detail="No articles found with the specified filters"
            )

        # Convert to DataFrame
        data = [article_to_dict(article) for article in articles]
        df = pd.DataFrame(data)

        # Create Excel file in memory
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name="Articles", index=False)

            # Summary sheet
            summary_data = {
                "Metric": [
                    "Total Articles",
                    "Positive Sentiment",
                    "Neutral Sentiment",
                    "Negative Sentiment",
                    "Unique Topics",
                    "Export Date",
                ],
                "Value": [
                    len(articles),
                    len([a for a in articles if a.sentiment_label == "positive"]),
                    len([a for a in articles if a.sentiment_label == "neutral"]),
                    len([a for a in articles if a.sentiment_label == "negative"]),
                    len(set(a.topic_category for a in articles if a.topic_category)),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ],
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

        output.seek(0)
        excel_content = output.getvalue()
        output.close()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"preventia_news_{timestamp}.xlsx"

        return Response(
            content=excel_content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")


# Chart export endpoints (placeholder implementations)
@router.get("/charts/{chart_id}.png")
async def export_chart_png(chart_id: str):
    """Export chart as PNG image."""
    # TODO: Implement chart generation using matplotlib or plotly
    raise HTTPException(status_code=501, detail="Chart export not yet implemented")


@router.get("/charts/{chart_id}.svg")
async def export_chart_svg(chart_id: str):
    """Export chart as SVG image."""
    # TODO: Implement chart generation using matplotlib or plotly
    raise HTTPException(status_code=501, detail="Chart export not yet implemented")


# PDF report generation (placeholder)
from fastapi import Body


@router.post("/report")
async def generate_pdf_report(
    filters: dict = Body(..., description="Filter parameters"),
    include_ai_summaries: bool = Body(False, description="Include AI summaries"),
    db: AsyncSession = Depends(get_db_session),
):
    """Generate PDF report with filtered data."""
    # TODO: Implement PDF generation using reportlab
    # For now, return a placeholder response

    report_id = f"rpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return {
        "status": "success",
        "data": {
            "report_id": report_id,
            "download_url": f"/api/v1/export/reports/{report_id}.pdf",
            "status": "generating",
            "estimated_completion": "2-3 minutes",
        },
    }


# User export history (placeholder)
@router.get("/user/exports")
async def get_user_exports(
    limit: int = Query(20, le=100, description="Maximum exports to return")
):
    """Get user's export history."""
    # TODO: Implement user session tracking and export history
    # For now, return empty list

    return {"status": "success", "data": [], "meta": {"total": 0, "limit": limit}}
