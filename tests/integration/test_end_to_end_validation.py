"""
End-to-End Validation Test Suite for PreventIA News Analytics
Comprehensive validation of the entire system functionality
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

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


@pytest.mark.e2e
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.database
class TestEndToEndSystemValidation:
    """Complete end-to-end system validation"""

    @pytest.fixture
    async def full_system_environment(self, test_db_manager):
        """Setup complete system environment for e2e testing"""
        async with test_db_manager.get_session() as session:
            # Clean all tables
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

    @pytest.fixture
    def comprehensive_test_dataset(self):
        """Provide comprehensive test dataset representing real-world scenarios"""
        return {
            "sources": [
                {
                    "name": "Medical News Network",
                    "base_url": "https://medicalnews.network",
                    "language": "en",
                    "country": "US",
                    "type": "medical_journal",
                },
                {
                    "name": "Global Health Today",
                    "base_url": "https://globalhealth.today",
                    "language": "en",
                    "country": "UK",
                    "type": "news_site",
                },
                {
                    "name": "Noticias Médicas",
                    "base_url": "https://noticias-medicas.es",
                    "language": "es",
                    "country": "ES",
                    "type": "news_site",
                },
            ],
            "articles": [
                # Positive sentiment articles
                {
                    "source_index": 0,
                    "title": "Breakthrough Gene Therapy Cures 95% of Breast Cancer Patients in Trial",
                    "url": "https://medicalnews.network/gene-therapy-breakthrough-2024",
                    "summary": "Revolutionary gene therapy treatment shows unprecedented success in Phase III trials for advanced breast cancer, offering hope for previously untreatable cases.",
                    "content": "A groundbreaking gene therapy approach has demonstrated remarkable efficacy in treating advanced breast cancer, with 95% of patients showing complete remission in a multicenter Phase III clinical trial. The treatment, developed by researchers at Johns Hopkins and Stanford, uses modified immune cells to target and destroy cancer cells while preserving healthy tissue. Dr. Maria Rodriguez, lead investigator, described the results as 'transformative for cancer treatment.' The therapy is now fast-tracked for FDA approval and could be available to patients within 18 months.",
                    "published_at": datetime.now() - timedelta(hours=1),
                    "expected_sentiment": "positive",
                    "expected_keywords": [
                        "gene therapy",
                        "breast cancer",
                        "clinical trial",
                        "FDA approval",
                    ],
                },
                {
                    "source_index": 1,
                    "title": "New Immunotherapy Drug Eliminates Tumors in 80% of Patients",
                    "url": "https://globalhealth.today/immunotherapy-success-2024",
                    "summary": "A novel immunotherapy drug has shown remarkable success in eliminating tumors in 80% of breast cancer patients with no significant side effects.",
                    "content": "Researchers at Oxford University announced extraordinary results from their latest immunotherapy study, where a new drug called ImmunoMax eliminated tumors completely in 80% of breast cancer patients. Unlike traditional chemotherapy, the treatment had minimal side effects and actually strengthened patients' immune systems. The drug works by enhancing the body's natural ability to recognize and destroy cancer cells.",
                    "published_at": datetime.now() - timedelta(hours=3),
                    "expected_sentiment": "positive",
                    "expected_keywords": [
                        "immunotherapy",
                        "tumors",
                        "breast cancer",
                        "Oxford",
                    ],
                },
                # Negative sentiment articles
                {
                    "source_index": 0,
                    "title": "Rising Breast Cancer Deaths Among Young Women Sparks Global Concern",
                    "url": "https://medicalnews.network/young-women-cancer-deaths-2024",
                    "summary": "Alarming statistics show a 40% increase in breast cancer mortality among women under 35, prompting urgent calls for improved screening protocols.",
                    "content": "Global health authorities are expressing serious concern over a dramatic 40% increase in breast cancer deaths among women under 35 over the past five years. The increase is attributed to delayed diagnoses, aggressive tumor types, and limited screening for younger demographics. Dr. Sarah Chen from the World Health Organization stated that immediate action is needed to address this crisis. Environmental factors and lifestyle changes are being investigated as potential contributors to this troubling trend.",
                    "published_at": datetime.now() - timedelta(hours=5),
                    "expected_sentiment": "negative",
                    "expected_keywords": [
                        "breast cancer",
                        "mortality",
                        "young women",
                        "screening",
                    ],
                },
                {
                    "source_index": 1,
                    "title": "Critical Drug Shortage Leaves Thousands Without Cancer Treatment",
                    "url": "https://globalhealth.today/drug-shortage-crisis-2024",
                    "summary": "A severe shortage of essential chemotherapy drugs is forcing doctors to ration treatments and delay procedures for breast cancer patients worldwide.",
                    "content": "Healthcare systems globally are struggling with a critical shortage of key chemotherapy medications, forcing difficult decisions about patient care. Over 25,000 breast cancer patients are currently affected by treatment delays or protocol modifications. Manufacturing issues, supply chain disruptions, and increased demand have created what medical professionals are calling the worst drug shortage in decades. Hospitals are implementing emergency protocols and seeking alternative treatments.",
                    "published_at": datetime.now() - timedelta(hours=8),
                    "expected_sentiment": "negative",
                    "expected_keywords": [
                        "drug shortage",
                        "chemotherapy",
                        "treatment delays",
                        "breast cancer",
                    ],
                },
                # Neutral sentiment articles
                {
                    "source_index": 0,
                    "title": "FDA Approves Standard Mammography Protocol Update",
                    "url": "https://medicalnews.network/fda-mammography-update-2024",
                    "summary": "The FDA has approved updated guidelines for mammography screening procedures, incorporating new technical standards and reporting requirements.",
                    "content": "The Food and Drug Administration announced the approval of updated mammography screening guidelines that include new technical standards for imaging equipment and standardized reporting protocols. The changes, which take effect next year, are designed to improve consistency across healthcare facilities and enhance early detection capabilities. Healthcare providers will need to complete additional training to comply with the new requirements.",
                    "published_at": datetime.now() - timedelta(hours=12),
                    "expected_sentiment": "neutral",
                    "expected_keywords": [
                        "FDA",
                        "mammography",
                        "guidelines",
                        "screening",
                    ],
                },
                {
                    "source_index": 2,
                    "title": "Conferencia Internacional sobre Investigación del Cáncer de Mama",
                    "url": "https://noticias-medicas.es/conferencia-cancer-mama-2024",
                    "summary": "La conferencia anual reúne a investigadores de todo el mundo para compartir avances en el tratamiento del cáncer de mama.",
                    "content": "La Conferencia Internacional sobre Investigación del Cáncer de Mama se celebra esta semana en Madrid, reuniendo a más de 2,000 investigadores, médicos y especialistas de 50 países. Durante los tres días de evento se presentarán los últimos avances en diagnóstico, tratamiento y prevención. Los temas principales incluyen terapias personalizadas, medicina de precisión y nuevas tecnologías de imagen.",
                    "published_at": datetime.now() - timedelta(hours=16),
                    "expected_sentiment": "neutral",
                    "expected_keywords": [
                        "conferencia",
                        "investigación",
                        "cáncer de mama",
                        "Madrid",
                    ],
                },
            ],
        }

    @pytest.mark.asyncio
    async def test_complete_system_workflow_validation(
        self, full_system_environment, comprehensive_test_dataset
    ):
        """Validate complete system workflow with comprehensive dataset"""

        # Step 1: System Health Check
        client = TestClient(app)
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"

        # Step 2: Data Ingestion Simulation
        sources_created = []
        async with full_system_environment.get_session() as session:
            for source_data in comprehensive_test_dataset["sources"]:
                source = NewsSource(
                    name=source_data["name"],
                    base_url=source_data["base_url"],
                    language=source_data["language"],
                    country=source_data["country"],
                    is_active=True,
                    validation_status="validated",
                )
                session.add(source)
                sources_created.append(source)

            await session.commit()
            for source in sources_created:
                await session.refresh(source)

        # Step 3: Article Processing Pipeline
        articles_created = []
        for article_data in comprehensive_test_dataset["articles"]:
            source = sources_created[article_data["source_index"]]
            async with full_system_environment.get_session() as session:
                article = Article(
                    source_id=source.id,
                    title=article_data["title"],
                    url=article_data["url"],
                    summary=article_data["summary"],
                    content=article_data["content"],
                    published_at=article_data["published_at"],
                    scraped_at=datetime.now(),
                    processing_status="pending",
                    language=source.language,
                    country=source.country,
                )
                session.add(article)
                articles_created.append((article, article_data))
                await session.commit()
                await session.refresh(article)

        # Step 4: NLP Processing and Validation
        sentiment_analyzer = get_sentiment_analyzer()
        nlp_results = []

        for article, expected_data in articles_created:
            shared_article = SharedArticle(
                title=article.title,
                published_at=article.published_at,
                summary=article.summary,
                content=article.content,
                url=article.url,
            )

            nlp_result = analyze_article(shared_article)
            nlp_results.append(nlp_result)

            # Validate NLP results
            assert (
                nlp_result.is_relevant
            ), f"Article should be relevant: {article.title}"
            assert nlp_result.sentiment_data["sentiment_label"] in [
                "positive",
                "negative",
                "neutral",
            ]
            assert 0.0 <= nlp_result.sentiment_data["confidence"] <= 1.0
            assert len(nlp_result.matched_keywords) >= 1

            # Update database
            async with full_system_environment.get_session() as session:
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
                for keyword in nlp_result.matched_keywords[:3]:
                    keyword_entry = ArticleKeyword(
                        article_id=article.id,
                        keyword=keyword,
                        relevance_score=0.8,
                        keyword_type="medical_term",
                    )
                    session.add(keyword_entry)

                await session.commit()

        # Step 5: API Endpoint Validation
        # Test articles endpoint
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        articles_data = response.json()
        assert len(articles_data) == 6  # All test articles

        # Verify each article has required fields
        for article_data in articles_data:
            assert "id" in article_data
            assert "title" in article_data
            assert "url" in article_data
            assert "sentiment_label" in article_data
            assert article_data["sentiment_label"] in [
                "positive",
                "negative",
                "neutral",
            ]

        # Test analytics endpoints
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        sentiment_analytics = response.json()
        assert "distribution" in sentiment_analytics

        # Verify sentiment distribution matches expectations
        sentiment_dist = sentiment_analytics["distribution"]
        assert sentiment_dist.get("positive", 0) >= 2  # We have 2 positive articles
        assert sentiment_dist.get("negative", 0) >= 2  # We have 2 negative articles
        assert sentiment_dist.get("neutral", 0) >= 2  # We have 2 neutral articles

        # Test search functionality
        response = client.get("/api/v1/articles/search", params={"q": "therapy"})
        assert response.status_code == 200
        search_results = response.json()
        therapy_articles = [
            a
            for a in search_results
            if "therapy" in a["title"].lower()
            or "therapy" in a.get("summary", "").lower()
        ]
        assert len(therapy_articles) >= 1

        # Test multilingual support
        response = client.get("/api/v1/articles/", params={"language": "es"})
        assert response.status_code == 200
        spanish_articles = response.json()
        spanish_count = len([a for a in spanish_articles if a.get("language") == "es"])
        assert spanish_count >= 1  # We have Spanish articles

        # Step 6: Data Consistency Validation
        async with full_system_environment.get_session() as session:
            # Verify all articles are processed
            total_articles = await session.execute(select(func.count(Article.id)))
            assert total_articles.scalar() == 6

            analyzed_articles = await session.execute(
                select(func.count(Article.id)).where(
                    Article.processing_status == "analyzed"
                )
            )
            assert analyzed_articles.scalar() == 6

            # Verify keywords were extracted
            total_keywords = await session.execute(
                select(func.count(ArticleKeyword.id))
            )
            assert total_keywords.scalar() >= 12  # At least 2 keywords per article

            # Verify geographic distribution
            geo_stats = await session.execute(
                select(Article.country, func.count(Article.id)).group_by(
                    Article.country
                )
            )
            geo_dist = dict(geo_stats.fetchall())
            assert "US" in geo_dist
            assert "UK" in geo_dist
            assert "ES" in geo_dist

    @pytest.mark.asyncio
    async def test_system_performance_under_load(self, full_system_environment):
        """Test system performance under simulated load"""

        # Create performance test dataset
        start_time = time.time()

        async with full_system_environment.get_session() as session:
            # Create 50 sources
            sources = []
            for i in range(50):
                source = NewsSource(
                    name=f"Performance Source {i+1}",
                    base_url=f"https://perf-source-{i+1}.com",
                    language="en",
                    country="US",
                    is_active=True,
                )
                session.add(source)
                sources.append(source)

            await session.commit()
            for source in sources:
                await session.refresh(source)

            # Create 200 articles (4 per source)
            articles = []
            for i, source in enumerate(sources):
                for j in range(4):
                    article = Article(
                        source_id=source.id,
                        title=f"Performance Article {i*4 + j + 1}",
                        url=f"https://perf-source-{i+1}.com/article-{j+1}",
                        summary=f"Performance test summary {i*4 + j + 1}",
                        content=f"Performance test content for article {i*4 + j + 1}. "
                        * 20,
                        published_at=datetime.now() - timedelta(hours=j),
                        scraped_at=datetime.now(),
                        processing_status="analyzed",
                        sentiment_score=0.1 * (j - 2),  # Varied sentiment scores
                        sentiment_label=(
                            "positive"
                            if j % 3 == 0
                            else "negative" if j % 3 == 1 else "neutral"
                        ),
                    )
                    session.add(article)
                    articles.append(article)

            await session.commit()

        data_creation_time = time.time() - start_time

        # Test API performance with load
        client = TestClient(app)
        api_test_start = time.time()

        # Test multiple concurrent requests
        import concurrent.futures

        def make_api_request(endpoint):
            start = time.time()
            response = client.get(endpoint)
            duration = time.time() - start
            return response.status_code, duration, len(response.content)

        endpoints = [
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
            "/api/v1/analytics/topics",
            "/api/v1/articles/stats",
            "/health",
        ]

        # Test concurrent API calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for _ in range(100):  # 100 total requests
                endpoint = endpoints[_ % len(endpoints)]
                future = executor.submit(make_api_request, endpoint)
                futures.append(future)

            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        api_test_time = time.time() - api_test_start
        total_time = time.time() - start_time

        # Performance assertions
        assert (
            data_creation_time < 30.0
        ), f"Data creation took too long: {data_creation_time}s"
        assert api_test_time < 60.0, f"API testing took too long: {api_test_time}s"
        assert total_time < 90.0, f"Total performance test took too long: {total_time}s"

        # API response quality
        successful_requests = [r for r in results if r[0] == 200]
        assert (
            len(successful_requests) >= 95
        ), f"Too many failed requests: {len(successful_requests)}/100"

        # Response times should be reasonable
        avg_response_time = sum(r[1] for r in successful_requests) / len(
            successful_requests
        )
        assert (
            avg_response_time < 2.0
        ), f"Average response time too slow: {avg_response_time}s"

    @pytest.mark.asyncio
    async def test_system_error_recovery_and_resilience(self, full_system_environment):
        """Test system error recovery and resilience"""

        client = TestClient(app)

        # Test API resilience with invalid requests
        error_scenarios = [
            ("/api/v1/articles/999999", 404),  # Non-existent article
            ("/api/v1/articles/?page=-1", 422),  # Invalid pagination
            ("/api/v1/articles/search", 422),  # Missing query parameter
            ("/api/invalid-endpoint", 404),  # Non-existent endpoint
        ]

        for endpoint, expected_status in error_scenarios:
            response = client.get(endpoint)
            assert response.status_code == expected_status

            # Error responses should be properly formatted
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                assert "detail" in error_data

        # Test database error handling
        async with full_system_environment.get_session() as session:
            source = NewsSource(
                name="Error Recovery Test",
                base_url="https://error-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Create article with edge case data
            problematic_article = Article(
                source_id=source.id,
                title="",  # Empty title
                url="https://error-test.com/empty",
                summary=None,  # Null summary
                content="",  # Empty content
                published_at=datetime.now(),
                scraped_at=datetime.now(),
                processing_status="pending",
            )
            session.add(problematic_article)
            await session.commit()

        # API should handle problematic data gracefully
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        articles_data = response.json()

        # Should include the problematic article without crashing
        empty_title_articles = [
            a for a in articles_data if not a.get("title", "").strip()
        ]
        assert len(empty_title_articles) >= 1

    def test_api_documentation_and_schema_validation(self):
        """Test API documentation and schema validation"""

        client = TestClient(app)

        # Test OpenAPI schema is accessible
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_schema = response.json()
        assert "openapi" in openapi_schema
        assert "info" in openapi_schema
        assert "paths" in openapi_schema

        # Verify essential endpoints are documented
        paths = openapi_schema["paths"]
        essential_endpoints = [
            "/health",
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
            "/api/v1/articles/search",
        ]

        for endpoint in essential_endpoints:
            assert endpoint in paths, f"Essential endpoint {endpoint} not documented"

        # Test interactive documentation is accessible
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()

    @pytest.mark.asyncio
    async def test_data_integrity_and_validation(self, full_system_environment):
        """Test comprehensive data integrity and validation"""

        # Create test data with specific characteristics
        async with full_system_environment.get_session() as session:
            source = NewsSource(
                name="Integrity Test Source",
                base_url="https://integrity-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Create articles with known sentiment and keywords
            test_cases = [
                {
                    "title": "Amazing Breakthrough in Cancer Treatment",
                    "content": "This breakthrough treatment is excellent and shows wonderful results",
                    "expected_sentiment": "positive",
                },
                {
                    "title": "Terrible News: Cancer Rates Increase Dramatically",
                    "content": "This horrible situation shows terrible outcomes and devastating results",
                    "expected_sentiment": "negative",
                },
                {
                    "title": "Standard Medical Report on Cancer Statistics",
                    "content": "The report shows standard statistics and regular medical data",
                    "expected_sentiment": "neutral",
                },
            ]

            articles = []
            for i, case in enumerate(test_cases):
                article = Article(
                    source_id=source.id,
                    title=case["title"],
                    url=f"https://integrity-test.com/article-{i+1}",
                    summary=case["content"][:100],
                    content=case["content"],
                    published_at=datetime.now() - timedelta(hours=i),
                    scraped_at=datetime.now(),
                    processing_status="pending",
                )
                session.add(article)
                articles.append(article)

            await session.commit()
            for article in articles:
                await session.refresh(article)

        # Process with NLP and validate sentiment accuracy
        sentiment_analyzer = get_sentiment_analyzer()

        for i, (article, case) in enumerate(zip(articles, test_cases)):
            shared_article = SharedArticle(
                title=article.title,
                published_at=article.published_at,
                summary=article.summary,
                content=article.content,
                url=article.url,
            )

            nlp_result = analyze_article(shared_article)
            detected_sentiment = nlp_result.sentiment_data["sentiment_label"]

            # Update database
            async with full_system_environment.get_session() as session:
                db_article = await session.get(Article, article.id)
                db_article.sentiment_label = detected_sentiment
                db_article.processing_status = "analyzed"
                await session.commit()

        # Validate data consistency through API
        client = TestClient(app)

        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        articles_data = response.json()

        # Verify all articles have sentiment labels
        for article_data in articles_data:
            assert "sentiment_label" in article_data
            assert article_data["sentiment_label"] in [
                "positive",
                "negative",
                "neutral",
            ]

        # Test analytics consistency
        response = client.get("/api/v1/analytics/sentiment")
        assert response.status_code == 200
        analytics_data = response.json()

        # Manual count should match analytics
        manual_sentiment_count = {}
        for article_data in articles_data:
            label = article_data["sentiment_label"]
            manual_sentiment_count[label] = manual_sentiment_count.get(label, 0) + 1

        analytics_distribution = analytics_data["distribution"]
        for label, count in manual_sentiment_count.items():
            assert analytics_distribution.get(label, 0) == count


@pytest.mark.e2e
@pytest.mark.performance
class TestSystemPerformanceBenchmarks:
    """Performance benchmarks for the complete system"""

    def test_api_response_time_benchmarks(self):
        """Test API response time benchmarks"""

        client = TestClient(app)

        # Define performance benchmarks
        endpoints_benchmarks = [
            ("/health", 1.0),  # Health check should be very fast
            ("/api/v1/articles/", 5.0),  # Articles listing
            ("/api/v1/analytics/sentiment", 10.0),  # Analytics can be slower
            ("/api/v1/analytics/topics", 10.0),  # Topic analytics
            ("/docs", 3.0),  # Documentation
        ]

        for endpoint, max_time in endpoints_benchmarks:
            start_time = time.time()
            response = client.get(endpoint)
            duration = time.time() - start_time

            assert response.status_code == 200, f"Endpoint {endpoint} failed"
            assert (
                duration < max_time
            ), f"Endpoint {endpoint} too slow: {duration:.2f}s > {max_time}s"

    def test_concurrent_request_handling(self):
        """Test concurrent request handling performance"""

        import concurrent.futures
        import threading

        client = TestClient(app)

        def make_concurrent_request():
            start_time = time.time()
            response = client.get("/api/v1/articles/")
            duration = time.time() - start_time
            return response.status_code, duration

        # Test with 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_concurrent_request) for _ in range(20)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All requests should succeed
        successful_requests = [r for r in results if r[0] == 200]
        assert (
            len(successful_requests) >= 18
        ), f"Too many failed concurrent requests: {len(successful_requests)}/20"

        # Average response time should remain reasonable under load
        avg_time = sum(r[1] for r in successful_requests) / len(successful_requests)
        assert (
            avg_time < 5.0
        ), f"Average response time under load too slow: {avg_time:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
