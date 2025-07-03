"""
Integration tests for legacy API endpoints.
Tests the backward compatibility layer for v1 endpoints.
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.integration
class TestLegacyAPIEndpoints:
    """Test legacy API endpoints for backward compatibility."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_get_news_legacy_success(self, client):
        """Test /api/v1/news endpoint returns paginated articles."""
        response = client.get("/api/v1/news")

        assert response.status_code == 200
        data = response.json()

        # Check legacy format structure
        assert "status" in data
        assert data["status"] == "success"
        assert "data" in data
        assert "meta" in data

        # Check pagination meta
        meta = data["meta"]
        assert "page" in meta
        assert "page_size" in meta
        assert "total" in meta
        assert meta["page"] == 1
        assert meta["page_size"] == 20

        # Check articles structure
        articles = data["data"]
        assert isinstance(articles, list)

        if articles:  # If we have articles
            article = articles[0]
            required_fields = [
                "id",
                "title",
                "summary",
                "url",
                "date",
                "topic",
                "tone",
                "country",
                "language",
            ]
            for field in required_fields:
                assert field in article, f"Missing field: {field}"

            # Check data types
            assert isinstance(article["id"], str)
            assert isinstance(article["title"], str)
            assert isinstance(article["url"], str)
            assert isinstance(article["date"], str)
            assert article["tone"] in ["positive", "negative", "neutral"]

    def test_get_news_legacy_pagination(self, client):
        """Test pagination parameters work correctly."""
        response = client.get("/api/v1/news?page=2&page_size=5")

        assert response.status_code == 200
        data = response.json()

        meta = data["meta"]
        assert meta["page"] == 2
        assert meta["page_size"] == 5
        assert len(data["data"]) <= 5

    def test_get_news_legacy_filters(self, client):
        """Test filtering parameters work correctly."""
        # Test topic filter
        response = client.get("/api/v1/news?topic=treatment")
        assert response.status_code == 200

        # Test date range filter
        date_from = "2024-01-01"
        date_to = "2024-12-31"
        response = client.get(f"/api/v1/news?date_from={date_from}&date_to={date_to}")
        assert response.status_code == 200

        # Test search filter
        response = client.get("/api/v1/news?search=cancer")
        assert response.status_code == 200

    def test_get_news_detail_legacy_success(self, client):
        """Test /api/v1/news/{id} endpoint returns article details."""
        # First get list to get a valid ID
        list_response = client.get("/api/v1/news")

        assert list_response.status_code == 200
        articles = list_response.json()["data"]

        if articles:
            article_id = articles[0]["id"]

            detail_response = client.get(f"/api/v1/news/{article_id}")

            assert detail_response.status_code == 200
            data = detail_response.json()

            assert data["status"] == "success"
            assert "data" in data
            article = data["data"]

            # Check all required fields
            required_fields = [
                "id",
                "title",
                "summary",
                "url",
                "date",
                "topic",
                "tone",
                "country",
                "language",
            ]
            for field in required_fields:
                assert field in article

    def test_get_news_detail_legacy_not_found(self, client):
        """Test /api/v1/news/{id} returns 404 for non-existent article."""
        response = client.get("/api/v1/news/999999")

        assert response.status_code == 200  # Legacy API returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert data["code"] == 404

    def test_get_news_detail_legacy_invalid_id(self, client):
        """Test /api/v1/news/{id} returns 400 for invalid article ID."""
        response = client.get("/api/v1/news/invalid_id")

        assert response.status_code == 200  # Legacy API returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert data["code"] == 400

    def test_get_stats_summary_legacy(self, client):
        """Test /api/v1/stats/summary endpoint returns KPI summary."""
        response = client.get("/api/v1/stats/summary")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        summary = data["data"]
        required_fields = ["week", "total", "countries", "tones"]
        for field in required_fields:
            assert field in summary

        # Check tones structure
        tones = summary["tones"]
        assert "positive" in tones
        assert "negative" in tones
        assert "neutral" in tones

        # Check data types
        assert isinstance(summary["week"], int)
        assert isinstance(summary["total"], int)
        assert isinstance(summary["countries"], int)
        assert isinstance(tones["positive"], int)
        assert isinstance(tones["negative"], int)
        assert isinstance(tones["neutral"], int)

    def test_get_stats_summary_legacy_with_week(self, client):
        """Test /api/v1/stats/summary endpoint with week parameter."""
        response = client.get("/api/v1/stats/summary?week=10")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        summary = data["data"]
        assert summary["week"] == 10

    def test_get_stats_topics_legacy(self, client):
        """Test /api/v1/stats/topics endpoint returns topic distribution."""
        response = client.get("/api/v1/stats/topics")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        topics = data["data"]
        assert isinstance(topics, dict)

        # Check that all values are integers
        for topic, count in topics.items():
            assert isinstance(topic, str)
            assert isinstance(count, int)
            assert count >= 0

    def test_get_stats_topics_legacy_with_filters(self, client):
        """Test /api/v1/stats/topics with date filters."""
        response = client.get(
            "/api/v1/stats/topics?date_from=2024-01-01&date_to=2024-12-31"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_stats_tones_legacy(self, client):
        """Test /api/v1/stats/tones endpoint returns tone distribution."""
        response = client.get("/api/v1/stats/tones")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        tones = data["data"]
        assert isinstance(tones, dict)

        # Check required tone categories
        required_tones = ["positive", "negative", "neutral"]
        for tone in required_tones:
            assert tone in tones
            assert isinstance(tones[tone], int)
            assert tones[tone] >= 0

    def test_get_stats_tones_legacy_with_filters(self, client):
        """Test /api/v1/stats/tones with date filters."""
        response = client.get(
            "/api/v1/stats/tones?date_from=2024-01-01&date_to=2024-12-31"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_tones_timeline_legacy(self, client):
        """Test /api/v1/stats/tones/timeline endpoint returns time series data."""
        response = client.get("/api/v1/stats/tones/timeline")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        timeline = data["data"]
        required_fields = ["labels", "positive", "negative", "neutral"]
        for field in required_fields:
            assert field in timeline
            assert isinstance(timeline[field], list)

        # Check that all arrays have the same length
        if timeline["labels"]:
            length = len(timeline["labels"])
            assert len(timeline["positive"]) == length
            assert len(timeline["negative"]) == length
            assert len(timeline["neutral"]) == length

    def test_get_tones_timeline_legacy_with_weeks(self, client):
        """Test /api/v1/stats/tones/timeline with weeks parameter."""
        response = client.get("/api/v1/stats/tones/timeline?weeks=4")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_stats_geo_legacy(self, client):
        """Test /api/v1/stats/geo endpoint returns geographic distribution."""
        response = client.get("/api/v1/stats/geo")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "data" in data

        geo_data = data["data"]
        assert isinstance(geo_data, list)

        if geo_data:
            entry = geo_data[0]
            required_fields = ["country", "total", "tone", "language"]
            for field in required_fields:
                assert field in entry

            assert isinstance(entry["country"], str)
            assert isinstance(entry["total"], int)
            assert isinstance(entry["tone"], str)
            assert isinstance(entry["language"], str)
            assert entry["tone"] in ["positive", "negative", "neutral"]

    def test_get_stats_geo_legacy_with_filters(self, client):
        """Test /api/v1/stats/geo with filters."""
        response = client.get("/api/v1/stats/geo?date_from=2024-01-01&topic=treatment")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_legacy_format_consistency(self, client):
        """Test that all legacy endpoints return consistent format."""
        endpoints = [
            "/api/v1/news",
            "/api/v1/stats/summary",
            "/api/v1/stats/topics",
            "/api/v1/stats/tones",
            "/api/v1/stats/tones/timeline",
            "/api/v1/stats/geo",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)

            assert response.status_code == 200
            data = response.json()

            # All legacy endpoints should have status field
            assert "status" in data
            assert data["status"] == "success"
            assert "data" in data

    def test_legacy_error_handling(self, client):
        """Test error handling in legacy endpoints."""
        # Test invalid date format
        response = client.get("/api/v1/news?date_from=invalid-date")
        # Should handle gracefully (might return 400, 422 or ignore invalid date)
        assert response.status_code in [200, 400, 422]

        # Test invalid pagination
        response = client.get("/api/v1/news?page=0")
        assert response.status_code == 422  # Should reject invalid page

        # Test invalid page size
        response = client.get("/api/v1/news?page_size=1000")
        assert response.status_code == 422  # Should reject too large page size
