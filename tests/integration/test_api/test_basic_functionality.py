"""
Basic integration tests for FastAPI functionality.
"""

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.integration
@pytest.mark.database
class TestBasicAPIFunctionality:
    """Test basic API functionality."""

    def test_root_endpoint(self):
        """Test root API endpoint."""
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "PreventIA News Analytics API"
        assert data["version"] == "1.0.0"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code in [200, 503]  # May be unhealthy in test env
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_articles_endpoint_basic(self):
        """Test basic articles endpoint."""
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

    def test_dashboard_endpoint_basic(self):
        """Test basic dashboard endpoint."""
        client = TestClient(app)
        response = client.get("/api/analytics/dashboard")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "total_articles" in data
        assert "recent_articles" in data
        assert "analysis_period_days" in data

    def test_nlp_status_endpoint(self):
        """Test NLP status endpoint."""
        client = TestClient(app)
        response = client.get("/api/nlp/analyzers/status")

        assert response.status_code == 200
        data = response.json()

        assert "sentiment_analyzer" in data
        assert "topic_classifier" in data
        assert "system_status" in data
