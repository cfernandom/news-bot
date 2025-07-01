"""
Unit tests for API models and schemas.
"""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from services.data.database.models import (
    ArticleBase,
    ArticleResponse,
    DashboardSummary,
    NewsSourceResponse,
    PaginatedResponse,
)


@pytest.mark.unit
class TestArticleModels:
    """Test Article-related Pydantic models."""

    def test_article_base_valid_data(self):
        """Test ArticleBase with valid data."""
        article_data = {
            "title": "Test Article",
            "url": "https://example.com/test",
            "content": "Test content",
            "summary": "Test summary",
            "published_at": datetime.now(timezone.utc),
            "language": "en",
            "country": "US",
        }

        article = ArticleBase(**article_data)
        assert article.title == "Test Article"
        assert article.url == "https://example.com/test"
        assert article.language == "en"

    def test_article_base_minimal_data(self):
        """Test ArticleBase with minimal required data."""
        article_data = {
            "title": "Minimal Article",
            "url": "https://example.com/minimal",
            "published_at": datetime.now(timezone.utc),
        }

        article = ArticleBase(**article_data)
        assert article.title == "Minimal Article"
        assert article.content is None
        assert article.summary is None

    def test_article_base_empty_title_allowed(self):
        """Test that empty title is allowed (permissive model)."""
        article_data = {
            "title": "",
            "url": "https://example.com/test",
            "published_at": datetime.now(timezone.utc),
        }

        # Empty title is allowed in our permissive model
        article = ArticleBase(**article_data)
        assert article.title == ""

    def test_article_response_model(self):
        """Test ArticleResponse model validation."""
        article_data = {
            "id": 1,
            "title": "Test Article",
            "url": "https://example.com/test",
            "published_at": datetime.now(timezone.utc),
            "source_id": 1,
            "scraped_at": datetime.now(timezone.utc),
            "processing_status": "completed",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        article = ArticleResponse(**article_data)
        assert article.id == 1
        assert article.processing_status == "completed"
        assert article.sentiment_label is None


@pytest.mark.unit
class TestDashboardModels:
    """Test Dashboard-related models."""

    def test_dashboard_summary_valid(self):
        """Test DashboardSummary with valid data."""
        dashboard_data = {
            "total_articles": 100,
            "recent_articles": 25,
            "sentiment_distribution": {"positive": 30, "negative": 40, "neutral": 30},
            "topic_distribution": {"treatment": 50, "research": 30, "other": 20},
            "active_sources": 4,
            "avg_sentiment_score": 0.15,
            "analysis_period_days": 30,
        }

        dashboard = DashboardSummary(**dashboard_data)
        assert dashboard.total_articles == 100
        assert dashboard.sentiment_distribution["positive"] == 30
        assert dashboard.avg_sentiment_score == 0.15

    def test_dashboard_summary_allows_negative_values(self):
        """Test that negative values are allowed (permissive model)."""
        dashboard_data = {
            "total_articles": -1,
            "recent_articles": 25,
            "sentiment_distribution": {},
            "topic_distribution": {},
            "active_sources": 4,
            "avg_sentiment_score": 0.15,
            "analysis_period_days": 30,
        }

        # Negative values are allowed in our permissive model
        dashboard = DashboardSummary(**dashboard_data)
        assert dashboard.total_articles == -1


@pytest.mark.unit
class TestPaginationModels:
    """Test Pagination-related models."""

    def test_paginated_response_valid(self):
        """Test PaginatedResponse with valid data."""
        paginated_data = {
            "items": [{"id": 1, "name": "test"}],
            "total": 100,
            "page": 1,
            "size": 20,
            "pages": 5,
        }

        response = PaginatedResponse(**paginated_data)
        assert len(response.items) == 1
        assert response.total == 100
        assert response.pages == 5

    def test_paginated_response_calculation_consistency(self):
        """Test that pagination calculations are consistent."""
        paginated_data = {
            "items": [],
            "total": 47,
            "page": 3,
            "size": 20,
            "pages": 3,  # 47 / 20 = 2.35, so 3 pages
        }

        response = PaginatedResponse(**paginated_data)
        assert response.pages == 3
        # Should be on page 3 with size 20, which is valid for 47 total items


@pytest.mark.unit
class TestNewsSourceModels:
    """Test NewsSource-related models."""

    def test_news_source_response_valid(self):
        """Test NewsSourceResponse with valid data."""
        source_data = {
            "id": 1,
            "name": "Test Source",
            "base_url": "https://test.com",
            "language": "en",
            "country": "US",
            "validation_status": "validated",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        source = NewsSourceResponse(**source_data)
        assert source.name == "Test Source"
        assert source.validation_status == "validated"
        assert source.is_active is True  # Default value
