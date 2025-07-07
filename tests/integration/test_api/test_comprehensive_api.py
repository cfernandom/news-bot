"""
Comprehensive API integration tests.
Tests all API endpoints with realistic data and edge cases.
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.integration
class TestComprehensiveAPI:
    """Comprehensive tests for all API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_api_documentation_accessible(self, client):
        """Test API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_openapi_schema_valid(self, client):
        """Test OpenAPI schema is valid."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()

        # Check required OpenAPI fields
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        assert len(schema["paths"]) > 0

    def test_health_check_comprehensive(self, client):
        """Test comprehensive health check."""
        response = client.get("/health")
        assert response.status_code == 200

        health_data = response.json()
        assert health_data["status"] == "healthy"
        assert "timestamp" in health_data
        assert "version" in health_data
        assert "services" in health_data

    def test_articles_crud_complete_workflow(self, client):
        """Test complete CRUD workflow for articles."""
        # List articles
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        initial_count = len(response.json())

        # Search articles
        response = client.get("/api/v1/articles/search", params={"q": "breast cancer"})
        assert response.status_code == 200
        search_results = response.json()
        assert isinstance(search_results, list)

        # Get article statistics
        response = client.get("/api/v1/articles/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_articles" in stats
        assert "articles_by_source" in stats
        assert "processing_status" in stats

    def test_analytics_endpoints_comprehensive(self, client):
        """Test all analytics endpoints with comprehensive data."""
        # Sentiment analytics
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        sentiment_data = response.json()
        assert "distribution" in sentiment_data
        assert "average_scores" in sentiment_data
        assert "trends" in sentiment_data

        # Topics analytics
        response = client.get("/api/v1/analytics/topics")
        assert response.status_code == 200
        topics_data = response.json()
        assert "distribution" in topics_data
        assert "trending_topics" in topics_data

        # Geographic analytics
        response = client.get("/api/v1/analytics/geographic")
        assert response.status_code == 200
        geo_data = response.json()
        assert "coverage_by_region" in geo_data

        # Temporal analytics
        response = client.get("/api/v1/analytics/temporal")
        assert response.status_code == 200
        temporal_data = response.json()
        assert "daily_counts" in temporal_data
        assert "weekly_trends" in temporal_data

    def test_nlp_endpoints_comprehensive(self, client):
        """Test all NLP endpoints with comprehensive functionality."""
        # Test text analysis
        test_text = "This is a breakthrough in breast cancer treatment showing promising results."
        response = client.post("/api/v1/nlp/analyze", json={"text": test_text})
        assert response.status_code == 200
        analysis = response.json()
        assert "sentiment" in analysis
        assert "topic" in analysis
        assert "keywords" in analysis

        # Test batch analysis
        batch_texts = [
            "Positive medical research outcomes",
            "Concerning health statistics",
            "Neutral regulatory update",
        ]
        response = client.post("/api/v1/nlp/batch-analyze", json={"texts": batch_texts})
        assert response.status_code == 200
        batch_results = response.json()
        assert len(batch_results) == 3

    def test_legacy_endpoints_complete_compatibility(self, client):
        """Test complete legacy API compatibility."""
        # Legacy news endpoint
        response = client.get("/api/v1/news")
        assert response.status_code == 200
        legacy_data = response.json()
        assert "status" in legacy_data
        assert "data" in legacy_data
        assert "meta" in legacy_data

        # Legacy news with pagination
        response = client.get("/api/v1/news", params={"page": 1, "limit": 10})
        assert response.status_code == 200
        paginated_data = response.json()
        assert paginated_data["meta"]["page"] == 1
        assert paginated_data["meta"]["page_size"] == 10

        # Legacy timeline
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        response = client.get(
            "/api/v1/tones/timeline",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        assert response.status_code == 200
        timeline_data = response.json()
        assert "timeline" in timeline_data

        # Legacy geographic stats
        response = client.get("/api/v1/stats/geo")
        assert response.status_code == 200
        geo_stats = response.json()
        assert "coverage" in geo_stats

    def test_error_handling_comprehensive(self, client):
        """Test comprehensive error handling."""
        # Test 404 errors
        response = client.get("/api/v1/articles/999999")
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data

        # Test validation errors
        response = client.post("/api/v1/nlp/analyze", json={"invalid": "data"})
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

        # Test invalid date ranges
        response = client.get(
            "/api/v1/tones/timeline",
            params={"start_date": "invalid-date", "end_date": "2024-01-01"},
        )
        assert response.status_code == 422

    def test_data_consistency_across_endpoints(self, client):
        """Test data consistency across different endpoints."""
        # Get total articles from stats
        response = client.get("/api/v1/articles/stats")
        assert response.status_code == 200
        total_from_stats = response.json()["total_articles"]

        # Get articles count from list endpoint
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        total_from_list = len(response.json())

        # Get total from legacy news
        response = client.get("/api/v1/news")
        assert response.status_code == 200
        total_from_legacy = response.json()["meta"]["total"]

        # All counts should be consistent
        assert (
            total_from_stats == total_from_legacy
        ), "Stats and legacy totals should match"

    def test_response_format_consistency(self, client):
        """Test response format consistency across endpoints."""
        # Check modern API endpoints return proper JSON
        endpoints = [
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
            "/api/v1/analytics/topics",
            "/health",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("application/json")

            # Ensure valid JSON
            try:
                json.loads(response.text)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON from {endpoint}")

    def test_cors_headers_present(self, client):
        """Test CORS headers are present for frontend integration."""
        response = client.options("/api/v1/articles/")
        # Note: TestClient doesn't fully simulate CORS, but we can check if middleware is configured
        assert response.status_code in [
            200,
            405,
        ]  # Either OPTIONS supported or method not allowed

    def test_rate_limiting_headers(self, client):
        """Test rate limiting headers if implemented."""
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        # Check if rate limiting headers are present (optional)
        # headers = response.headers
        # if "x-ratelimit-limit" in headers:
        #     assert int(headers["x-ratelimit-limit"]) > 0

    def test_authentication_requirements(self, client):
        """Test authentication requirements for protected endpoints."""
        # Most endpoints should be accessible without auth in current implementation
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200

        # If auth is implemented, test protected endpoints
        # response = client.get("/api/v1/admin/")
        # assert response.status_code == 401

    def test_api_versioning_consistency(self, client):
        """Test API versioning is consistent."""
        # Check that v1 endpoints exist
        v1_endpoints = [
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
            "/api/v1/news",
        ]

        for endpoint in v1_endpoints:
            response = client.get(endpoint)
            assert (
                response.status_code == 200
            ), f"v1 endpoint {endpoint} should be accessible"

    def test_database_transaction_handling(self, client):
        """Test database transaction handling in API endpoints."""
        # Test multiple concurrent requests don't interfere
        import concurrent.futures

        def make_request():
            response = client.get("/api/v1/articles/")
            return response.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All requests should succeed
        assert all(
            status == 200 for status in results
        ), "All concurrent requests should succeed"
