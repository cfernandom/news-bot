"""
Performance tests for FastAPI endpoints.
Ensures all endpoints meet performance requirements (<5s response time).
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pytest
import requests
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.performance
class TestAPIPerformance:
    """Performance tests for critical API endpoints."""

    BASE_URL = "http://localhost:8000"

    @pytest.fixture
    def client(self):
        """Create test client that uses live server."""
        # Try live server first, fallback to TestClient
        try:
            response = requests.get(f"{self.BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                return "live_server"
        except:
            pass
        return TestClient(app)

    def measure_endpoint_time(
        self, client, method: str, endpoint: str, **kwargs
    ) -> float:
        """Measure response time for an endpoint."""
        start_time = time.time()

        if client == "live_server":
            # Use requests for live server
            url = f"{self.BASE_URL}{endpoint}"
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                response = requests.post(url, **kwargs)
            elif method.upper() == "PUT":
                response = requests.put(url, **kwargs)
            elif method.upper() == "DELETE":
                response = requests.delete(url, **kwargs)
        else:
            # Use TestClient
            if method.upper() == "GET":
                response = client.get(endpoint, **kwargs)
            elif method.upper() == "POST":
                response = client.post(endpoint, **kwargs)
            elif method.upper() == "PUT":
                response = client.put(endpoint, **kwargs)
            elif method.upper() == "DELETE":
                response = client.delete(endpoint, **kwargs)

        end_time = time.time()

        # Ensure request succeeded
        assert response.status_code in [
            200,
            201,
            204,
        ], f"Request failed with status {response.status_code}: {response.text if hasattr(response, 'text') else 'N/A'}"

        return end_time - start_time

    def test_health_check_performance(self, client):
        """Test health check endpoint performance."""
        response_time = self.measure_endpoint_time(client, "GET", "/health")
        assert (
            response_time < 1.0
        ), f"Health check took {response_time:.3f}s, expected <1s"

    def test_articles_list_performance(self, client):
        """Test articles list endpoint performance."""
        response_time = self.measure_endpoint_time(client, "GET", "/api/v1/articles/")
        assert (
            response_time < 5.0
        ), f"Articles list took {response_time:.3f}s, expected <5s"

    def test_articles_search_performance(self, client):
        """Test articles search endpoint performance."""
        response_time = self.measure_endpoint_time(
            client,
            "GET",
            "/api/v1/articles/search",
            params={"q": "breast cancer", "limit": 20},
        )
        assert (
            response_time < 5.0
        ), f"Articles search took {response_time:.3f}s, expected <5s"

    def test_analytics_sentiment_performance(self, client):
        """Test sentiment analytics endpoint performance."""
        response_time = self.measure_endpoint_time(
            client, "GET", "/api/v1/analytics/sentiment"
        )
        assert (
            response_time < 5.0
        ), f"Sentiment analytics took {response_time:.3f}s, expected <5s"

    def test_analytics_topics_performance(self, client):
        """Test topics analytics endpoint performance."""
        response_time = self.measure_endpoint_time(
            client, "GET", "/api/v1/analytics/topics"
        )
        assert (
            response_time < 5.0
        ), f"Topics analytics took {response_time:.3f}s, expected <5s"

    def test_analytics_geographic_performance(self, client):
        """Test geographic analytics endpoint performance."""
        response_time = self.measure_endpoint_time(
            client, "GET", "/api/v1/analytics/geographic"
        )
        assert (
            response_time < 5.0
        ), f"Geographic analytics took {response_time:.3f}s, expected <5s"

    def test_legacy_news_performance(self, client):
        """Test legacy news endpoint performance."""
        response_time = self.measure_endpoint_time(client, "GET", "/api/v1/news")
        assert (
            response_time < 5.0
        ), f"Legacy news took {response_time:.3f}s, expected <5s"

    def test_legacy_timeline_performance(self, client):
        """Test legacy timeline endpoint performance."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        response_time = self.measure_endpoint_time(
            client,
            "GET",
            "/api/v1/tones/timeline",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        assert (
            response_time < 5.0
        ), f"Legacy timeline took {response_time:.3f}s, expected <5s"

    def test_concurrent_requests_performance(self, client):
        """Test concurrent request handling performance."""
        import concurrent.futures
        import threading

        def make_request():
            return self.measure_endpoint_time(client, "GET", "/health")

        # Test 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            start_time = time.time()
            futures = [executor.submit(make_request) for _ in range(10)]
            response_times = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]
            total_time = time.time() - start_time

        # All individual requests should be fast
        max_response_time = max(response_times)
        assert (
            max_response_time < 2.0
        ), f"Slowest concurrent request took {max_response_time:.3f}s"

        # Total time should be reasonable (not serialized)
        assert total_time < 5.0, f"10 concurrent requests took {total_time:.3f}s total"

    def test_memory_usage_under_load(self, client):
        """Test memory usage doesn't grow excessively under load."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Make 50 requests
        for i in range(50):
            response = client.get("/api/v1/articles/")
            assert response.status_code == 200

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory shouldn't increase by more than 100MB
        assert (
            memory_increase < 100
        ), f"Memory increased by {memory_increase:.1f}MB under load"

    @pytest.mark.parametrize(
        "endpoint,method,params",
        [
            ("/api/v1/articles/", "GET", {}),
            ("/api/v1/analytics/sentiment", "GET", {}),
            ("/api/v1/analytics/topics", "GET", {}),
            ("/api/v1/analytics/geographic", "GET", {}),
            ("/api/v1/news", "GET", {}),
            ("/health", "GET", {}),
            ("/api/v1/articles/search", "GET", {"params": {"q": "cancer"}}),
        ],
    )
    def test_all_endpoints_performance_baseline(self, client, endpoint, method, params):
        """Test all critical endpoints meet 5s performance baseline."""
        response_time = self.measure_endpoint_time(client, method, endpoint, **params)
        assert (
            response_time < 5.0
        ), f"{endpoint} took {response_time:.3f}s, expected <5s"
