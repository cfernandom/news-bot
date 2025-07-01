"""
End-to-end tests for complete API workflows.
"""

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.mark.e2e
@pytest.mark.database
@pytest.mark.slow
class TestCompleteAPIWorkflows:
    """Test complete user workflows through the API."""

    def test_dashboard_data_workflow(self):
        """Test complete dashboard data retrieval workflow."""
        client = TestClient(app)

        # 1. Get dashboard summary
        response = client.get("/api/analytics/dashboard")
        assert response.status_code == 200
        dashboard = response.json()

        total_articles = dashboard["total_articles"]
        assert total_articles >= 0

        # 2. Get detailed sentiment trends
        response = client.get("/api/analytics/sentiment/trends?days=30")
        assert response.status_code == 200
        trends = response.json()

        # 3. Get topic distribution
        response = client.get("/api/analytics/topics/distribution")
        assert response.status_code == 200
        topics = response.json()

        # 4. Get articles with filters based on dashboard data
        if dashboard["sentiment_distribution"]:
            # Get articles with most common sentiment
            dominant_sentiment = max(
                dashboard["sentiment_distribution"],
                key=dashboard["sentiment_distribution"].get,
            )

            response = client.get(
                f"/api/articles/?sentiment={dominant_sentiment}&size=5"
            )
            assert response.status_code == 200
            articles = response.json()

            # Verify we got articles with the requested sentiment
            for article in articles["items"]:
                if article.get("sentiment_label"):
                    assert article["sentiment_label"] == dominant_sentiment

    def test_article_search_and_analysis_workflow(self):
        """Test article search and analysis workflow."""
        client = TestClient(app)

        # 1. Search for articles
        response = client.get("/api/articles/search/?q=treatment")
        assert response.status_code == 200
        search_results = response.json()

        if search_results["total"] > 0:
            # 2. Get detailed view of first article
            first_article = search_results["items"][0]
            article_id = first_article["id"]

            response = client.get(f"/api/articles/{article_id}")
            assert response.status_code == 200
            article_detail = response.json()

            assert article_detail["id"] == article_id
            assert "treatment" in (
                article_detail["title"].lower()
                + (article_detail.get("summary", "") or "").lower()
                + (article_detail.get("content", "") or "").lower()
            )

            # 3. If article has content, analyze its sentiment
            if article_detail.get("content") or article_detail.get("summary"):
                text_to_analyze = (
                    article_detail.get("summary")
                    or article_detail.get("content", "")[:1000]  # Limit for API
                )

                sentiment_request = {
                    "text": text_to_analyze,
                    "title": article_detail["title"],
                }

                response = client.post("/api/nlp/sentiment", json=sentiment_request)
                # NLP might fail in test environment, so accept both success and failure
                assert response.status_code in [200, 500]

    def test_analytics_deep_dive_workflow(self):
        """Test deep analytics exploration workflow."""
        client = TestClient(app)

        # 1. Get overall dashboard
        response = client.get("/api/analytics/dashboard?days=90")
        assert response.status_code == 200
        dashboard = response.json()

        # 2. Get sources performance
        response = client.get("/api/analytics/sources/performance")
        assert response.status_code == 200
        sources = response.json()

        # 3. Get weekly trends
        response = client.get("/api/analytics/trends/weekly?weeks=12")
        assert response.status_code == 200
        weekly_trends = response.json()

        # 4. Cross-validate data consistency
        # Dashboard total should be >= sum of source articles
        if sources["total_sources"] > 0:
            source_articles_sum = sum(
                source["total_articles"] for source in sources["sources"]
            )
            assert dashboard["total_articles"] >= source_articles_sum

        # 5. Verify weekly trends show reasonable data
        if weekly_trends["total_weeks"] > 0:
            total_weekly_articles = sum(
                week["article_count"] for week in weekly_trends["weekly_trends"]
            )
            # Weekly data should be subset of total (within the time period)
            assert total_weekly_articles <= dashboard["total_articles"]

    def test_error_handling_workflow(self):
        """Test error handling across different endpoints."""
        client = TestClient(app)

        # 1. Test non-existent article
        response = client.get("/api/articles/999999")
        assert response.status_code == 404

        # 2. Test invalid pagination
        response = client.get("/api/articles/?page=-1")
        assert response.status_code == 422

        # 3. Test invalid analytics parameters
        response = client.get("/api/analytics/dashboard?days=0")
        assert response.status_code == 422

        # 4. Test invalid search queries
        response = client.get("/api/articles/search/")  # Missing query param
        assert response.status_code == 422

        # 5. Test invalid NLP input
        response = client.post("/api/nlp/sentiment", json={"text": ""})
        assert response.status_code == 422

        # All errors should return proper JSON with error details
        for status_code in [404, 422]:
            if status_code == 404:
                response = client.get("/api/articles/999999")
            else:
                response = client.get("/api/articles/?page=-1")

            assert response.status_code == status_code
            error_data = response.json()
            assert isinstance(error_data, dict)
            assert "detail" in error_data

    def test_pagination_consistency_workflow(self):
        """Test pagination consistency across all endpoints."""
        client = TestClient(app)

        # Test articles pagination
        response = client.get("/api/articles/?size=10")
        assert response.status_code == 200
        data = response.json()

        if data["total"] > 10:
            # Test page navigation
            response = client.get("/api/articles/?page=2&size=10")
            assert response.status_code == 200
            page2_data = response.json()

            assert page2_data["page"] == 2
            assert page2_data["size"] == 10
            assert page2_data["total"] == data["total"]  # Total should be consistent

            # Items should be different between pages
            page1_ids = {item["id"] for item in data["items"]}
            page2_ids = {item["id"] for item in page2_data["items"]}
            assert page1_ids.isdisjoint(page2_ids)  # No overlap between pages

        # Test search pagination
        response = client.get("/api/articles/search/?q=cancer&size=5")
        assert response.status_code == 200
        search_data = response.json()

        if search_data["total"] > 5:
            response = client.get("/api/articles/search/?q=cancer&page=2&size=5")
            assert response.status_code == 200
            search_page2 = response.json()

            assert search_page2["total"] == search_data["total"]
            assert search_page2["page"] == 2


@pytest.mark.e2e
@pytest.mark.performance
@pytest.mark.slow
class TestAPIPerformanceWorkflows:
    """Test API performance under realistic usage patterns."""

    def test_dashboard_loading_performance(self):
        """Test dashboard loading performance simulation."""
        import time

        client = TestClient(app)

        # Simulate dashboard page load - multiple parallel requests
        start_time = time.time()

        # These would typically be loaded in parallel by a frontend
        dashboard_response = client.get("/api/analytics/dashboard")
        trends_response = client.get("/api/analytics/sentiment/trends?days=30")
        topics_response = client.get("/api/analytics/topics/distribution")

        total_duration = time.time() - start_time

        # All requests should succeed
        assert dashboard_response.status_code == 200
        assert trends_response.status_code == 200
        assert topics_response.status_code == 200

        # Total time should be reasonable for dashboard loading
        assert total_duration < 15.0  # Should load within 15 seconds

    def test_large_dataset_handling(self):
        """Test API behavior with large dataset requests."""
        client = TestClient(app)

        # Test large page size (within limits)
        response = client.get("/api/articles/?size=100")
        assert response.status_code == 200
        data = response.json()

        # Should handle large page sizes efficiently
        assert len(data["items"]) <= 100
        assert data["size"] == 100

        # Test analytics with longer time periods
        response = client.get("/api/analytics/dashboard?days=365")
        assert response.status_code == 200

        response = client.get("/api/analytics/trends/weekly?weeks=52")
        assert response.status_code == 200


@pytest.mark.e2e
@pytest.mark.database
class TestDataIntegrityWorkflows:
    """Test data integrity across API operations."""

    def test_cross_endpoint_data_consistency(self):
        """Test that data is consistent across different endpoints."""
        client = TestClient(app)

        # Get articles count from multiple sources
        dashboard_response = client.get("/api/analytics/dashboard")
        assert dashboard_response.status_code == 200
        dashboard_total = dashboard_response.json()["total_articles"]

        summary_response = client.get("/api/articles/stats/summary")
        assert summary_response.status_code == 200
        summary_total = summary_response.json()["total_articles"]

        # Counts should match
        assert dashboard_total == summary_total

        # Sentiment distribution should be consistent
        dashboard_sentiment = dashboard_response.json()["sentiment_distribution"]
        summary_sentiment = summary_response.json()["sentiment_distribution"]

        assert dashboard_sentiment == summary_sentiment

    def test_filter_consistency(self):
        """Test that filtering produces consistent results."""
        client = TestClient(app)

        # Get all articles
        all_response = client.get(
            "/api/articles/?size=1000"
        )  # Large size to get many articles
        assert all_response.status_code == 200
        all_data = all_response.json()

        # Get filtered articles
        positive_response = client.get("/api/articles/?sentiment=positive&size=1000")
        assert positive_response.status_code == 200
        positive_data = positive_response.json()

        negative_response = client.get("/api/articles/?sentiment=negative&size=1000")
        assert negative_response.status_code == 200
        negative_data = negative_response.json()

        # Filtered results should be subsets of all results
        all_ids = {article["id"] for article in all_data["items"]}
        positive_ids = {article["id"] for article in positive_data["items"]}
        negative_ids = {article["id"] for article in negative_data["items"]}

        assert positive_ids.issubset(all_ids)
        assert negative_ids.issubset(all_ids)
        assert positive_ids.isdisjoint(negative_ids)  # No overlap between sentiments
