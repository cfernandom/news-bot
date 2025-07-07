"""
Complete System Integration Tests for PreventIA News Analytics
Tests the entire system flow: Scrapers → Database → NLP → API → Analytics
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.main import app
from services.data.database.connection import db_manager
from services.data.database.models import Article, ArticleKeyword, NewsSource
from services.nlp.src.analyzer import analyze_article
from services.nlp.src.sentiment import get_sentiment_analyzer
from services.shared.models.article import Article as SharedArticle


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.database
class TestCompleteSystemIntegration:
    """Test complete system integration workflows"""

    @pytest.fixture
    async def clean_test_data(self, test_db_manager):
        """Provide clean test environment and cleanup after test"""
        async with test_db_manager.get_session() as session:
            # Clean up any existing test data
            await session.execute(delete(ArticleKeyword))
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.commit()

        yield test_db_manager

        # Cleanup after test
        async with test_db_manager.get_session() as session:
            await session.execute(delete(ArticleKeyword))
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.commit()

    @pytest.mark.asyncio
    async def test_complete_news_processing_pipeline(self, clean_test_data):
        """Test complete pipeline: Source → Scraper → NLP → Database → API"""

        # Step 1: Create a news source in database
        async with clean_test_data.get_session() as session:
            test_source = NewsSource(
                name="Test Medical News",
                base_url="https://test.medical-news.com",
                language="en",
                country="US",
                is_active=True,
                validation_status="validated",
            )
            session.add(test_source)
            await session.commit()
            await session.refresh(test_source)
            source_id = test_source.id

        # Step 2: Simulate scraper creating articles
        test_articles_data = [
            {
                "title": "Breakthrough in Breast Cancer Treatment Shows 95% Success Rate",
                "url": "https://test.medical-news.com/breakthrough-treatment",
                "summary": "Revolutionary new chemotherapy protocol demonstrates unprecedented success rates in clinical trials for aggressive breast cancer cases.",
                "content": "A groundbreaking study published today reveals that a new combination chemotherapy protocol has achieved a 95% success rate in treating aggressive breast cancer. The treatment combines targeted therapy with immunotherapy, offering hope to thousands of patients.",
                "published_at": datetime.now() - timedelta(hours=2),
            },
            {
                "title": "Rising Concerns Over Late-Stage Cancer Diagnoses During Pandemic",
                "url": "https://test.medical-news.com/late-stage-diagnoses",
                "summary": "Healthcare professionals report alarming increases in late-stage breast cancer diagnoses as patients delayed screenings during COVID-19.",
                "content": "Medical experts are expressing serious concerns about a significant increase in late-stage breast cancer diagnoses. The COVID-19 pandemic led to delayed screenings and reduced healthcare access, resulting in more advanced cases when patients finally seek treatment.",
                "published_at": datetime.now() - timedelta(hours=4),
            },
            {
                "title": "FDA Approves New Diagnostic Imaging Technology",
                "url": "https://test.medical-news.com/fda-diagnostic-approval",
                "summary": "The FDA has approved a new AI-powered imaging technology for early detection of breast cancer.",
                "content": "The Food and Drug Administration announced approval of an advanced AI-powered imaging system that can detect breast cancer in earlier stages than traditional mammography. The technology uses machine learning algorithms to identify suspicious patterns.",
                "published_at": datetime.now() - timedelta(hours=6),
            },
        ]

        stored_articles = []
        async with clean_test_data.get_session() as session:
            for article_data in test_articles_data:
                # Create article in database (simulating scraper output)
                article = Article(
                    source_id=source_id,
                    title=article_data["title"],
                    url=article_data["url"],
                    summary=article_data["summary"],
                    content=article_data["content"],
                    published_at=article_data["published_at"],
                    scraped_at=datetime.now(),
                    processing_status="pending",
                )
                session.add(article)
                stored_articles.append(article)

            await session.commit()
            for article in stored_articles:
                await session.refresh(article)

        # Step 3: Process articles with NLP pipeline
        analyzer = get_sentiment_analyzer()

        for article in stored_articles:
            # Convert to shared model for NLP processing
            shared_article = SharedArticle(
                title=article.title,
                published_at=article.published_at,
                summary=article.summary,
                content=article.content,
                url=article.url,
            )

            # Analyze with NLP pipeline
            nlp_result = analyze_article(shared_article)

            # Update database with NLP results
            async with clean_test_data.get_session() as session:
                db_article = await session.get(Article, article.id)
                db_article.sentiment_score = nlp_result.sentiment_data["scores"][
                    "compound"
                ]
                db_article.sentiment_label = nlp_result.sentiment_data[
                    "sentiment_label"
                ]
                db_article.sentiment_confidence = nlp_result.sentiment_data[
                    "confidence"
                ]
                db_article.processing_status = "analyzed"

                # Add keywords
                for keyword in nlp_result.matched_keywords:
                    keyword_entry = ArticleKeyword(
                        article_id=article.id,
                        keyword=keyword,
                        relevance_score=0.8,  # Mock relevance score
                        keyword_type="medical_term",
                    )
                    session.add(keyword_entry)

                await session.commit()

        # Step 4: Test API endpoints return processed data
        client = TestClient(app)

        # Test articles endpoint
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        articles_data = response.json()
        assert len(articles_data) >= 3

        # Verify articles have sentiment analysis
        analyzed_articles = [a for a in articles_data if a.get("sentiment_label")]
        assert len(analyzed_articles) >= 3

        # Test analytics endpoints
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        sentiment_analytics = response.json()
        assert "distribution" in sentiment_analytics
        assert sum(sentiment_analytics["distribution"].values()) >= 3

        # Test that we have both positive and negative sentiments
        sentiments = [a["sentiment_label"] for a in analyzed_articles]
        assert "positive" in sentiments  # Breakthrough article
        assert "negative" in sentiments  # Concerning article

        # Step 5: Test search functionality
        response = client.get("/api/v1/articles/search", params={"q": "breakthrough"})
        assert response.status_code == 200
        search_results = response.json()
        breakthrough_articles = [
            a for a in search_results if "breakthrough" in a["title"].lower()
        ]
        assert len(breakthrough_articles) >= 1

        # Step 6: Test topic analytics
        response = client.get("/api/v1/analytics/topics")
        assert response.status_code == 200
        topics_data = response.json()
        assert "distribution" in topics_data

    @pytest.mark.asyncio
    async def test_data_consistency_across_system(self, clean_test_data):
        """Test data consistency across all system components"""

        # Create test data
        async with clean_test_data.get_session() as session:
            source = NewsSource(
                name="Consistency Test Source",
                base_url="https://consistency.test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Add multiple articles with known data
            articles = []
            for i in range(5):
                article = Article(
                    source_id=source.id,
                    title=f"Test Article {i+1}",
                    url=f"https://consistency.test.com/article-{i+1}",
                    summary=f"This is test article {i+1} with predictable content.",
                    published_at=datetime.now() - timedelta(hours=i),
                    scraped_at=datetime.now(),
                    sentiment_score=0.5 if i % 2 == 0 else -0.3,
                    sentiment_label="positive" if i % 2 == 0 else "negative",
                    processing_status="analyzed",
                )
                session.add(article)
                articles.append(article)

            await session.commit()
            for article in articles:
                await session.refresh(article)

        # Test consistency across different API endpoints
        client = TestClient(app)

        # Get total count from articles endpoint
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        all_articles = response.json()
        total_from_articles = len(all_articles)

        # Get total from stats endpoint
        response = client.get("/api/v1/articles/stats")
        assert response.status_code == 200
        stats = response.json()
        total_from_stats = stats["total_articles"]

        # Get total from legacy endpoint
        response = client.get("/api/v1/news")
        assert response.status_code == 200
        legacy_data = response.json()
        total_from_legacy = legacy_data["meta"]["total"]

        # All counts should be consistent
        assert total_from_articles == total_from_stats == total_from_legacy

        # Test sentiment distribution consistency
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        sentiment_data = response.json()

        # Count sentiments manually from articles
        positive_count = len(
            [a for a in all_articles if a.get("sentiment_label") == "positive"]
        )
        negative_count = len(
            [a for a in all_articles if a.get("sentiment_label") == "negative"]
        )

        # Compare with analytics
        analytics_positive = sentiment_data["distribution"].get("positive", 0)
        analytics_negative = sentiment_data["distribution"].get("negative", 0)

        assert positive_count == analytics_positive
        assert negative_count == analytics_negative

    @pytest.mark.asyncio
    async def test_error_resilience_across_system(self, clean_test_data):
        """Test system resilience to errors in different components"""

        # Test database connection resilience
        client = TestClient(app)

        # Test API when database has no data
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        assert response.json() == []

        # Test analytics with empty database
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        sentiment_data = response.json()
        assert sentiment_data["distribution"] == {}

        # Test search with no results
        response = client.get("/api/v1/articles/search", params={"q": "nonexistent"})
        assert response.status_code == 200
        assert response.json() == []

        # Test NLP with malformed data
        analyzer = get_sentiment_analyzer()
        result = analyzer.analyze_sentiment("", "")
        assert result["sentiment_label"] == "neutral"
        assert 0.0 <= result["confidence"] <= 1.0

    @pytest.mark.asyncio
    async def test_performance_under_load(self, clean_test_data):
        """Test system performance with larger datasets"""

        # Create larger test dataset
        async with clean_test_data.get_session() as session:
            source = NewsSource(
                name="Performance Test Source",
                base_url="https://perf.test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Create 50 articles to test performance
            articles = []
            for i in range(50):
                article = Article(
                    source_id=source.id,
                    title=f"Performance Test Article {i+1}",
                    url=f"https://perf.test.com/article-{i+1}",
                    summary=f"Performance test content for article {i+1}",
                    published_at=datetime.now() - timedelta(hours=i),
                    scraped_at=datetime.now(),
                    sentiment_score=0.1 * (i % 11 - 5),  # Varied scores
                    sentiment_label=(
                        "positive"
                        if i % 3 == 0
                        else "negative" if i % 3 == 1 else "neutral"
                    ),
                    processing_status="analyzed",
                )
                session.add(article)
                articles.append(article)

            await session.commit()

        # Test API performance with larger dataset
        import time

        client = TestClient(app)

        # Test articles endpoint performance
        start_time = time.time()
        response = client.get("/api/v1/articles/")
        articles_time = time.time() - start_time

        assert response.status_code == 200
        assert len(response.json()) >= 50
        assert articles_time < 5.0  # Should complete within 5 seconds

        # Test analytics performance
        start_time = time.time()
        response = client.get("/api/v1/analytics/sentiment")
        analytics_time = time.time() - start_time

        assert response.status_code == 200
        assert analytics_time < 3.0  # Analytics should be fast

        # Test search performance
        start_time = time.time()
        response = client.get("/api/v1/articles/search", params={"q": "performance"})
        search_time = time.time() - start_time

        assert response.status_code == 200
        assert search_time < 3.0  # Search should be reasonably fast

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, clean_test_data):
        """Test system behavior under concurrent operations"""

        import concurrent.futures
        import threading

        # Create test source
        async with clean_test_data.get_session() as session:
            source = NewsSource(
                name="Concurrent Test Source",
                base_url="https://concurrent.test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)
            source_id = source.id

        client = TestClient(app)

        def make_api_request(endpoint):
            """Helper function for concurrent requests"""
            try:
                response = client.get(endpoint)
                return response.status_code, len(
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json"
                    )
                    else []
                )
            except Exception as e:
                return 500, str(e)

        # Test concurrent API requests
        endpoints = [
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
            "/api/v1/analytics/topics",
            "/api/v1/articles/stats",
            "/health",
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Make multiple concurrent requests
            futures = []
            for _ in range(20):  # 20 concurrent requests
                endpoint = endpoints[_ % len(endpoints)]
                future = executor.submit(make_api_request, endpoint)
                futures.append(future)

            # Collect results
            results = []
            for future in concurrent.futures.as_completed(futures):
                status_code, response_size = future.result()
                results.append((status_code, response_size))

        # All requests should succeed
        successful_requests = [r for r in results if r[0] == 200]
        assert len(successful_requests) >= 18  # At least 90% should succeed

        # No request should take excessively long (this is implicit in the test completing)


@pytest.mark.integration
@pytest.mark.e2e
class TestSystemRecovery:
    """Test system recovery and resilience scenarios"""

    def test_api_graceful_degradation(self):
        """Test API graceful degradation when components fail"""
        client = TestClient(app)

        # Test that API responds even when some services might be down
        response = client.get("/health")
        assert response.status_code == 200

        # Test that invalid requests are handled gracefully
        response = client.get("/api/v1/articles/invalid-id")
        assert response.status_code == 404

        response = client.post("/api/v1/nlp/analyze", json={"invalid": "request"})
        assert response.status_code == 422

    def test_data_validation_robustness(self):
        """Test robustness of data validation across the system"""
        client = TestClient(app)

        # Test various edge cases
        test_cases = [
            # Empty parameters
            ("/api/v1/articles/search", {"q": ""}),
            # Very long parameters
            ("/api/v1/articles/search", {"q": "x" * 1000}),
            # Special characters
            ("/api/v1/articles/search", {"q": "!@#$%^&*()"}),
            # Invalid date ranges
            (
                "/api/v1/tones/timeline",
                {"start_date": "invalid", "end_date": "2024-01-01"},
            ),
        ]

        for endpoint, params in test_cases:
            response = client.get(endpoint, params=params)
            # Should either succeed or fail gracefully with proper error codes
            assert response.status_code in [200, 400, 422]

            if response.status_code != 200:
                # Error responses should have proper structure
                error_data = response.json()
                assert "detail" in error_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
