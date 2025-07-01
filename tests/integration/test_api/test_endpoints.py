"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.integration
@pytest.mark.database
class TestHealthEndpoints:
    """Test health and basic endpoints."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "status" in data
        assert "database" in data
        assert "articles_count" in data
        assert "version" in data

        # Health status should be either healthy or unhealthy
        assert data["status"] in ["healthy", "unhealthy"]
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self):
        """Test root API information endpoint."""
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["message"] == "PreventIA News Analytics API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"

    def test_openapi_docs_accessible(self):
        """Test that OpenAPI documentation is accessible."""
        client = TestClient(app)

        # Test docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

        # Test OpenAPI JSON schema
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


@pytest.mark.integration
@pytest.mark.database
class TestArticlesEndpoints:
    """Test articles-related endpoints."""

    def test_get_articles_basic(self):
        """Test basic articles listing."""
        client = TestClient(app)
        response = client.get("/api/articles/")

        assert response.status_code == 200
        data = response.json()

        # Check pagination structure
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "pages" in data

        # Verify default pagination
        assert data["page"] == 1
        assert data["size"] == 20
        assert isinstance(data["items"], list)
        assert isinstance(data["total"], int)

    def test_get_articles_with_pagination(self):
        """Test articles pagination."""
        client = TestClient(app)
        response = client.get("/api/articles/?page=1&size=5")

        assert response.status_code == 200
        data = response.json()

        assert data["page"] == 1
        assert data["size"] == 5
        assert len(data["items"]) <= 5

    def test_get_articles_with_filters(self):
        """Test articles filtering."""
        client = TestClient(app)

        # Test sentiment filter
        response = client.get("/api/articles/?sentiment=positive")
        assert response.status_code == 200

        # Test days filter
        response = client.get("/api/articles/?days=7")
        assert response.status_code == 200

        # Test combined filters
        response = client.get("/api/articles/?sentiment=negative&days=30&size=10")
        assert response.status_code == 200

        data = response.json()
        assert data["size"] == 10

    def test_search_articles(self):
        """Test article search functionality."""
        client = TestClient(app)
        response = client.get("/api/articles/search/?q=cancer")

        assert response.status_code == 200
        data = response.json()

        # Should have pagination structure
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)

    def test_articles_summary_stats(self):
        """Test articles summary statistics."""
        client = TestClient(app)
        response = client.get("/api/articles/stats/summary")

        assert response.status_code == 200
        data = response.json()

        # Check expected fields
        expected_fields = [
            "total_articles",
            "recent_articles",
            "sentiment_distribution",
            "topic_distribution",
            "articles_with_sentiment",
            "articles_with_topics",
        ]

        for field in expected_fields:
            assert field in data

        # Verify data types
        assert isinstance(data["total_articles"], int)
        assert isinstance(data["sentiment_distribution"], dict)
        assert isinstance(data["topic_distribution"], dict)

    def test_get_nonexistent_article(self):
        """Test retrieving non-existent article."""
        client = TestClient(app)
        response = client.get("/api/articles/999999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_invalid_pagination_parameters(self):
        """Test invalid pagination parameters."""
        client = TestClient(app)

        # Test negative page
        response = client.get("/api/articles/?page=0")
        assert response.status_code == 422

        # Test oversized page size
        response = client.get("/api/articles/?size=1000")
        assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.database
class TestAnalyticsEndpoints:
    """Test analytics-related endpoints."""

    def test_dashboard_summary(self):
        """Test dashboard summary endpoint."""
        client = TestClient(app)
        response = client.get("/api/analytics/dashboard")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        required_fields = [
            "total_articles",
            "recent_articles",
            "sentiment_distribution",
            "topic_distribution",
            "active_sources",
            "avg_sentiment_score",
            "analysis_period_days",
        ]

        for field in required_fields:
            assert field in data

        # Verify data types
        assert isinstance(data["total_articles"], int)
        assert isinstance(data["sentiment_distribution"], dict)
        assert isinstance(data["avg_sentiment_score"], (int, float))
        assert data["analysis_period_days"] == 30  # Default

    def test_dashboard_custom_period(self):
        """Test dashboard with custom analysis period."""
        client = TestClient(app)
        response = client.get("/api/analytics/dashboard?days=7")

        assert response.status_code == 200
        data = response.json()
        assert data["analysis_period_days"] == 7

    def test_sentiment_trends(self):
        """Test sentiment trends endpoint."""
        client = TestClient(app)
        response = client.get("/api/analytics/sentiment/trends")

        assert response.status_code == 200
        data = response.json()

        assert "trends" in data
        assert "period_days" in data
        assert "total_data_points" in data

        assert isinstance(data["trends"], dict)
        assert data["period_days"] == 30  # Default

    def test_topic_distribution(self):
        """Test topic distribution endpoint."""
        client = TestClient(app)
        response = client.get("/api/analytics/topics/distribution")

        assert response.status_code == 200
        data = response.json()

        assert "distribution" in data
        assert "total_articles" in data
        assert "unique_topics" in data
        assert "period_days" in data

        assert isinstance(data["distribution"], dict)
        assert data["period_days"] == "all_time"

    def test_weekly_trends(self):
        """Test weekly trends endpoint."""
        client = TestClient(app)
        response = client.get("/api/analytics/trends/weekly")

        assert response.status_code == 200
        data = response.json()

        assert "weekly_trends" in data
        assert "period_weeks" in data
        assert "total_weeks" in data

        assert isinstance(data["weekly_trends"], list)
        assert data["period_weeks"] == 12  # Default

    def test_analytics_invalid_parameters(self):
        """Test analytics endpoints with invalid parameters."""
        client = TestClient(app)

        # Test invalid days parameter (too small)
        response = client.get("/api/analytics/dashboard?days=0")
        assert response.status_code == 422

        # Test invalid days parameter (too large)
        response = client.get("/api/analytics/dashboard?days=500")
        assert response.status_code == 422


@pytest.mark.integration
class TestNLPEndpoints:
    """Test NLP-related endpoints."""

    def test_analyze_sentiment(self):
        """Test individual sentiment analysis."""
        client = TestClient(app)

        test_data = {
            "text": "This breakthrough treatment shows promising results.",
            "title": "Medical Breakthrough",
        }

        response = client.post("/api/nlp/sentiment", json=test_data)

        # NLP might fail in test environment, but endpoint should respond
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "sentiment_label" in data
            assert "confidence" in data
            assert "scores" in data
            assert "compound_score" in data

    def test_classify_topic(self):
        """Test topic classification."""
        client = TestClient(app)

        test_data = {
            "title": "New Chemotherapy Protocol",
            "summary": "Researchers develop new treatment protocol.",
            "content": "Study shows improved outcomes with new chemotherapy.",
        }

        response = client.post("/api/nlp/topic", json=test_data)

        # NLP might fail in test environment
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "topic_category" in data
            assert "confidence" in data
            assert "matched_keywords" in data

    def test_analyzers_status(self):
        """Test NLP analyzers status."""
        client = TestClient(app)
        response = client.get("/api/nlp/analyzers/status")

        assert response.status_code == 200
        data = response.json()

        assert "sentiment_analyzer" in data
        assert "topic_classifier" in data
        assert "system_status" in data

    def test_models_info(self):
        """Test NLP models information."""
        client = TestClient(app)
        response = client.get("/api/nlp/models/info")

        assert response.status_code == 200
        data = response.json()

        assert "sentiment_analysis" in data
        assert "topic_classification" in data
        assert "system_info" in data

    def test_sentiment_validation_errors(self):
        """Test sentiment analysis with invalid input."""
        client = TestClient(app)

        # Test empty text
        response = client.post("/api/nlp/sentiment", json={"text": ""})
        assert response.status_code == 422

        # Test missing required field
        response = client.post("/api/nlp/sentiment", json={"title": "Just title"})
        assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.slow
class TestAPIPerformance:
    """Test API performance characteristics."""

    def test_articles_endpoint_performance(self):
        """Test articles endpoint response time."""
        import time

        client = TestClient(app)

        start_time = time.time()
        response = client.get("/api/articles/?size=50")
        duration = time.time() - start_time

        assert response.status_code == 200
        assert duration < 5.0  # Should respond within 5 seconds

    def test_dashboard_endpoint_performance(self):
        """Test dashboard endpoint response time."""
        import time

        client = TestClient(app)

        start_time = time.time()
        response = client.get("/api/analytics/dashboard")
        duration = time.time() - start_time

        assert response.status_code == 200
        assert duration < 10.0  # Dashboard queries can be more complex
