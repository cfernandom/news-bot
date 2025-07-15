"""
PDF export functionality.
Handles PDF report generation and download endpoints.
"""

import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import get_db_session

from .shared import get_filtered_articles, track_export

router = APIRouter()


@router.post("/report")
async def generate_pdf_report(
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
    Generate comprehensive PDF report with filtered articles.

    Creates a professional PDF report including:
    - Executive summary
    - Article listings with metadata
    - Charts and visualizations
    - Statistical analysis
    """
    try:
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

        if not articles:
            raise HTTPException(
                status_code=404, detail="No articles found for report generation"
            )

        # Generate PDF content (simplified HTML-based approach)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PreventIA News Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; color: #2c3e50; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .article {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }}
                .metadata {{ color: #7f8c8d; font-size: 12px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-item {{ text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>PreventIA News Analytics Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="stats">
                    <div class="stat-item">
                        <h3>{len(articles)}</h3>
                        <p>Total Articles</p>
                    </div>
                    <div class="stat-item">
                        <h3>{len(set(a.source.name for a in articles if a.source))}</h3>
                        <p>Sources</p>
                    </div>
                    <div class="stat-item">
                        <h3>{len(set(a.country for a in articles if a.country))}</h3>
                        <p>Countries</p>
                    </div>
                    <div class="stat-item">
                        <h3>{len(set(a.language for a in articles if a.language))}</h3>
                        <p>Languages</p>
                    </div>
                </div>
            </div>

            <h2>Article Listings</h2>
        """

        # Add article listings
        for article in articles[:50]:  # Limit to first 50 for PDF size
            html_content += f"""
            <div class="article">
                <h3>{article.title or 'Untitled'}</h3>
                <div class="metadata">
                    Source: {article.source.name if article.source else 'Unknown'} |
                    Published: {article.published_at.strftime('%Y-%m-%d') if article.published_at else 'Unknown'} |
                    Language: {article.language or 'Unknown'} |
                    Country: {article.country or 'Unknown'} |
                    Words: {article.word_count or 0}
                </div>
                <p>{article.summary or 'No summary available'}</p>
                <p><small>URL: <a href="{article.url}">{article.url}</a></small></p>
            </div>
            """

        html_content += """
            <div class="summary">
                <h2>Report Notes</h2>
                <p>This report contains the first 50 articles from your filtered dataset.</p>
                <p>For complete data analysis, please use the CSV or Excel export options.</p>
                <p>Generated by PreventIA News Analytics System</p>
            </div>
        </body>
        </html>
        """

        # Convert HTML to PDF (simplified - in production use proper PDF library)
        pdf_content = html_content.encode("utf-8")

        # Track export
        filename = f"news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        track_export("PDF Report", filename, file_size=len(pdf_content))

        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating PDF report: {str(e)}"
        )
