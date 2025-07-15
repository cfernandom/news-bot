"""
Chart export functionality.
Handles chart generation and export endpoints.
"""

import base64
import io
from datetime import datetime
from typing import Any, Dict

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import get_db_session

from .shared import get_filtered_articles, track_export

matplotlib.use("Agg")  # Use non-interactive backend

router = APIRouter()


async def generate_sentiment_chart(
    db: AsyncSession, width: int = 10, height: int = 6, **filters
) -> str:
    """Generate sentiment analysis chart."""
    articles = await get_filtered_articles(db, **filters)

    if not articles:
        raise HTTPException(
            status_code=404, detail="No articles found for chart generation"
        )

    # Prepare data
    sentiment_data = []
    for article in articles:
        if article.sentiment_score:
            sentiment_data.append(
                {
                    "date": article.published_at,
                    "sentiment": article.sentiment_score,
                    "title": article.title,
                }
            )

    if not sentiment_data:
        raise HTTPException(status_code=404, detail="No sentiment data available")

    df = pd.DataFrame(sentiment_data)

    # Create chart
    plt.figure(figsize=(width, height))
    plt.plot(df["date"], df["sentiment"], marker="o", alpha=0.7)
    plt.title("Sentiment Analysis Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", dpi=300, bbox_inches="tight")
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    return img_str


async def generate_topics_chart(
    db: AsyncSession, width: int = 10, height: int = 6, **filters
) -> str:
    """Generate topics distribution chart."""
    articles = await get_filtered_articles(db, **filters)

    if not articles:
        raise HTTPException(
            status_code=404, detail="No articles found for chart generation"
        )

    # Simple topic analysis based on keywords
    topic_counts = {}
    keywords = ["cancer", "treatment", "research", "patient", "therapy", "study"]

    for article in articles:
        content = (article.title or "") + " " + (article.summary or "")
        content_lower = content.lower()

        for keyword in keywords:
            if keyword in content_lower:
                topic_counts[keyword] = topic_counts.get(keyword, 0) + 1

    if not topic_counts:
        raise HTTPException(status_code=404, detail="No topics found")

    # Create chart
    plt.figure(figsize=(width, height))
    topics = list(topic_counts.keys())
    counts = list(topic_counts.values())

    plt.bar(topics, counts, color="skyblue", alpha=0.7)
    plt.title("Topic Distribution")
    plt.xlabel("Topics")
    plt.ylabel("Article Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", dpi=300, bbox_inches="tight")
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    return img_str


async def generate_timeline_chart(
    db: AsyncSession, width: int = 12, height: int = 6, **filters
) -> str:
    """Generate timeline chart showing article publication over time."""
    articles = await get_filtered_articles(db, **filters)

    if not articles:
        raise HTTPException(
            status_code=404, detail="No articles found for chart generation"
        )

    # Prepare data
    dates = [article.published_at for article in articles if article.published_at]

    if not dates:
        raise HTTPException(status_code=404, detail="No publication dates available")

    # Create timeline
    df = pd.DataFrame({"date": dates})
    df["date"] = pd.to_datetime(df["date"])
    daily_counts = df.groupby(df["date"].dt.date).size()

    # Create chart
    plt.figure(figsize=(width, height))
    plt.plot(daily_counts.index, daily_counts.values, marker="o", linewidth=2)
    plt.title("Article Publication Timeline")
    plt.xlabel("Date")
    plt.ylabel("Number of Articles")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", dpi=300, bbox_inches="tight")
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode()
    plt.close()

    return img_str


@router.get("/charts/{chart_id}.png")
async def export_chart_png(chart_id: str, db: AsyncSession = Depends(get_db_session)):
    """Export chart as PNG image."""
    chart_generators = {
        "sentiment": generate_sentiment_chart,
        "topics": generate_topics_chart,
        "timeline": generate_timeline_chart,
    }

    if chart_id not in chart_generators:
        raise HTTPException(status_code=404, detail="Chart not found")

    try:
        img_str = await chart_generators[chart_id](db)
        img_data = base64.b64decode(img_str)

        # Track export
        filename = f"chart_{chart_id}_{int(datetime.now().timestamp())}.png"
        track_export("Chart PNG", filename, file_size=len(img_data))

        return Response(content=img_data, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chart: {str(e)}")


@router.get("/charts/{chart_id}.svg")
async def export_chart_svg(chart_id: str, db: AsyncSession = Depends(get_db_session)):
    """Export chart as SVG image."""
    chart_generators = {
        "sentiment": generate_sentiment_chart,
        "topics": generate_topics_chart,
        "timeline": generate_timeline_chart,
    }

    if chart_id not in chart_generators:
        raise HTTPException(status_code=404, detail="Chart not found")

    try:
        # Generate chart as SVG
        articles = await get_filtered_articles(db)

        if not articles:
            raise HTTPException(
                status_code=404, detail="No articles found for chart generation"
            )

        # Create a simple SVG chart (placeholder implementation)
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="300" fill="white"/>
  <text x="200" y="150" text-anchor="middle" font-size="16" fill="black">
    {chart_id.title()} Chart - {len(articles)} articles
  </text>
  <text x="200" y="170" text-anchor="middle" font-size="12" fill="gray">
    Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  </text>
</svg>"""

        # Track export
        filename = f"chart_{chart_id}_{int(datetime.now().timestamp())}.svg"
        track_export("Chart SVG", filename, file_size=len(svg_content))

        return Response(content=svg_content, media_type="image/svg+xml")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating SVG chart: {str(e)}"
        )
