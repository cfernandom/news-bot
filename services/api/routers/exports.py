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
from sqlalchemy import desc, func, or_, select, text
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
    import os
    import tempfile
    from io import BytesIO

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    # Create a temporary file for the PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    try:
        # Get comprehensive analytics data
        # 1. Basic sentiment stats
        sentiment_query = """
        SELECT
            COUNT(*) as total_articles,
            AVG(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) * 100 as positive_percentage,
            AVG(CASE WHEN sentiment_label = 'negative' THEN 1 ELSE 0 END) * 100 as negative_percentage,
            AVG(CASE WHEN sentiment_label = 'neutral' THEN 1 ELSE 0 END) * 100 as neutral_percentage
        FROM articles
        WHERE sentiment_label IS NOT NULL
        """

        # 2. Top sources
        sources_query = """
        SELECT ns.name as source_name, COUNT(*) as article_count
        FROM articles a
        JOIN news_sources ns ON a.source_id = ns.id
        GROUP BY ns.name
        ORDER BY article_count DESC
        LIMIT 5
        """

        # 3. Recent articles
        recent_query = """
        SELECT a.title, ns.name as source_name, a.sentiment_label,
               DATE(a.published_at) as publish_date
        FROM articles a
        JOIN news_sources ns ON a.source_id = ns.id
        WHERE a.sentiment_label IS NOT NULL
        ORDER BY a.published_at DESC
        LIMIT 10
        """

        # 4. Sentiment by source
        sentiment_by_source_query = """
        SELECT ns.name as source_name,
               COUNT(*) as total,
               AVG(CASE WHEN a.sentiment_label = 'positive' THEN 1 ELSE 0 END) * 100 as positive_pct,
               AVG(CASE WHEN a.sentiment_label = 'negative' THEN 1 ELSE 0 END) * 100 as negative_pct
        FROM articles a
        JOIN news_sources ns ON a.source_id = ns.id
        WHERE a.sentiment_label IS NOT NULL
        GROUP BY ns.name
        ORDER BY total DESC
        """

        # Execute all queries
        sentiment_result = await db.execute(text(sentiment_query))
        stats = sentiment_result.fetchone()

        sources_result = await db.execute(text(sources_query))
        top_sources = sources_result.fetchall()

        recent_result = await db.execute(text(recent_query))
        recent_articles = recent_result.fetchall()

        sentiment_by_source_result = await db.execute(text(sentiment_by_source_query))
        sentiment_by_source = sentiment_by_source_result.fetchall()

        # Create PDF
        doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
        story = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
        )

        # Title
        title = Paragraph("PreventIA Analytics Report", title_style)
        story.append(title)
        story.append(Spacer(1, 20))

        # Date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, styles["Normal"])
        story.append(date_para)
        story.append(Spacer(1, 20))

        # Analytics Summary
        summary_title = Paragraph("Analytics Summary", styles["Heading2"])
        story.append(summary_title)
        story.append(Spacer(1, 12))

        if stats:
            # Create summary table
            summary_data = [
                ["Metric", "Value"],
                [
                    "Total Articles Analyzed",
                    f"{int(stats.total_articles)}" if stats.total_articles else "0",
                ],
                [
                    "Positive Sentiment",
                    (
                        f"{stats.positive_percentage:.1f}%"
                        if stats.positive_percentage
                        else "0%"
                    ),
                ],
                [
                    "Negative Sentiment",
                    (
                        f"{stats.negative_percentage:.1f}%"
                        if stats.negative_percentage
                        else "0%"
                    ),
                ],
                [
                    "Neutral Sentiment",
                    (
                        f"{stats.neutral_percentage:.1f}%"
                        if stats.neutral_percentage
                        else "0%"
                    ),
                ],
            ]

            summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(summary_table)
        else:
            story.append(Paragraph("No analytics data available.", styles["Normal"]))

        story.append(Spacer(1, 30))

        # Top Sources Section
        sources_title = Paragraph("Top News Sources", styles["Heading2"])
        story.append(sources_title)
        story.append(Spacer(1, 12))

        if top_sources:
            sources_data = [["Source", "Articles"]]
            for source in top_sources:
                sources_data.append([source.source_name, str(source.article_count)])

            sources_table = Table(sources_data, colWidths=[4 * inch, 1 * inch])
            sources_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 11),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightblue),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(sources_table)

        story.append(Spacer(1, 30))

        # Sentiment by Source Section
        sentiment_source_title = Paragraph(
            "Sentiment Analysis by Source", styles["Heading2"]
        )
        story.append(sentiment_source_title)
        story.append(Spacer(1, 12))

        if sentiment_by_source:
            sentiment_source_data = [["Source", "Total", "Positive %", "Negative %"]]
            for row in sentiment_by_source:
                sentiment_source_data.append(
                    [
                        (
                            row.source_name[:30] + "..."
                            if len(row.source_name) > 30
                            else row.source_name
                        ),
                        str(row.total),
                        f"{row.positive_pct:.1f}%",
                        f"{row.negative_pct:.1f}%",
                    ]
                )

            sentiment_source_table = Table(
                sentiment_source_data,
                colWidths=[2.5 * inch, 0.8 * inch, 1 * inch, 1 * inch],
            )
            sentiment_source_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(sentiment_source_table)

        story.append(Spacer(1, 30))

        # Recent Articles Section
        recent_title = Paragraph("Recent Articles", styles["Heading2"])
        story.append(recent_title)
        story.append(Spacer(1, 12))

        if recent_articles:
            recent_data = [["Title", "Source", "Sentiment", "Date"]]
            for article in recent_articles:
                title_truncated = (
                    article.title[:40] + "..."
                    if len(article.title) > 40
                    else article.title
                )
                source_truncated = (
                    article.source_name[:20] + "..."
                    if len(article.source_name) > 20
                    else article.source_name
                )
                sentiment_emoji = {
                    "positive": "😊 Pos",
                    "negative": "😞 Neg",
                    "neutral": "😐 Neu",
                }.get(article.sentiment_label, article.sentiment_label)

                recent_data.append(
                    [
                        title_truncated,
                        source_truncated,
                        sentiment_emoji,
                        str(article.publish_date) if article.publish_date else "N/A",
                    ]
                )

            recent_table = Table(
                recent_data, colWidths=[2.5 * inch, 1.5 * inch, 0.8 * inch, 0.8 * inch]
            )
            recent_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.purple),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.lavender),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )

            story.append(recent_table)

        story.append(Spacer(1, 30))

        # Key Insights Section
        insights_title = Paragraph("Key Insights", styles["Heading2"])
        story.append(insights_title)
        story.append(Spacer(1, 12))

        if stats:
            # Generate insights based on data
            total_articles = int(stats.total_articles) if stats.total_articles else 0
            positive_pct = stats.positive_percentage or 0
            negative_pct = stats.negative_percentage or 0

            insights = []
            if total_articles > 0:
                insights.append(
                    f"• {total_articles} articles have been analyzed for sentiment"
                )
                if negative_pct > positive_pct:
                    insights.append(
                        f"• Negative sentiment dominates at {negative_pct:.1f}% vs {positive_pct:.1f}% positive"
                    )
                elif positive_pct > negative_pct:
                    insights.append(
                        f"• Positive sentiment prevails at {positive_pct:.1f}% vs {negative_pct:.1f}% negative"
                    )
                else:
                    insights.append(
                        f"• Sentiment is balanced between positive ({positive_pct:.1f}%) and negative ({negative_pct:.1f}%)"
                    )

                if top_sources:
                    top_source = top_sources[0]
                    insights.append(
                        f"• {top_source.source_name} is the most active source with {top_source.article_count} articles"
                    )

            for insight in insights:
                insight_para = Paragraph(insight, styles["Normal"])
                story.append(insight_para)
                story.append(Spacer(1, 8))

        story.append(Spacer(1, 20))

        # Methodology Section
        methodology_title = Paragraph("Methodology", styles["Heading2"])
        story.append(methodology_title)
        story.append(Spacer(1, 12))

        methodology_text = """
        This report uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis,
        specifically calibrated for medical content. The analysis considers contextual information and
        applies conservative thresholds appropriate for healthcare news coverage.
        """
        methodology_para = Paragraph(methodology_text, styles["Normal"])
        story.append(methodology_para)
        story.append(Spacer(1, 20))

        # Disclaimer Section
        disclaimer_title = Paragraph("Disclaimer", styles["Heading3"])
        story.append(disclaimer_title)
        story.append(Spacer(1, 8))

        disclaimer_text = """
        This analysis is for research and educational purposes only. The sentiment analysis reflects
        computational interpretation of text and should not be considered as medical advice or
        professional healthcare guidance.
        """
        disclaimer_para = Paragraph(disclaimer_text, styles["Normal"])
        story.append(disclaimer_para)
        story.append(Spacer(1, 20))

        # Footer
        footer_text = f"Generated by PreventIA Analytics Platform | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer_para = Paragraph(footer_text, styles["Normal"])
        story.append(footer_para)

        # Build PDF
        doc.build(story)

        # Read the PDF file
        with open(temp_file.name, "rb") as f:
            pdf_content = f.read()

        # Clean up
        os.unlink(temp_file.name)

        # Return PDF as response
        from fastapi.responses import Response

        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=preventia_analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            },
        )

    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
    finally:
        temp_file.close()


# User export history (placeholder)
@router.get("/user/exports")
async def get_user_exports(
    limit: int = Query(20, le=100, description="Maximum exports to return")
):
    """Get user's export history."""
    # TODO: Implement user session tracking and export history
    # For now, return empty list

    return {"status": "success", "data": [], "meta": {"total": 0, "limit": limit}}
