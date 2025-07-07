"""
Data Pipeline Integration Tests for PreventIA News Analytics
Tests the complete data flow: Sources → Scraping → Processing → Storage → Analytics
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import db_manager
from services.data.database.models import (
    Article,
    ArticleKeyword,
    NewsSource,
    WeeklyAnalytics,
)
from services.nlp.src.analyzer import analyze_article
from services.nlp.src.sentiment import get_sentiment_analyzer
from services.shared.models.article import Article as SharedArticle


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.database
class TestDataPipelineIntegration:
    """Test complete data pipeline integration"""

    @pytest.fixture
    async def clean_pipeline_environment(self, test_db_manager):
        """Provide clean environment for pipeline testing"""
        async with test_db_manager.get_session() as session:
            # Clean all data tables
            await session.execute(delete(WeeklyAnalytics))
            await session.execute(delete(ArticleKeyword))
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.commit()

        yield test_db_manager

        # Cleanup after test
        async with test_db_manager.get_session() as session:
            await session.execute(delete(WeeklyAnalytics))
            await session.execute(delete(ArticleKeyword))
            await session.execute(delete(Article))
            await session.execute(delete(NewsSource))
            await session.commit()

    @pytest.fixture
    def sample_news_data(self):
        """Provide realistic sample news data"""
        return [
            {
                "source": {
                    "name": "Medical Research Today",
                    "base_url": "https://medicalresearch.today",
                    "language": "en",
                    "country": "US",
                },
                "articles": [
                    {
                        "title": "Revolutionary Breast Cancer Treatment Shows 98% Success Rate in Clinical Trials",
                        "url": "https://medicalresearch.today/breakthrough-treatment-2024",
                        "summary": "A groundbreaking new immunotherapy treatment for aggressive breast cancer has demonstrated unprecedented success rates in Phase III clinical trials, offering new hope for patients with advanced disease.",
                        "content": "Researchers at leading medical centers have announced remarkable results from a Phase III clinical trial testing a novel immunotherapy approach for treating triple-negative breast cancer. The treatment, which combines checkpoint inhibitors with targeted therapy, achieved a 98% response rate in patients with previously untreatable advanced disease. Dr. Sarah Johnson, lead researcher, stated that this represents the most significant advancement in breast cancer treatment in decades.",
                        "published_at": datetime.now() - timedelta(hours=2),
                        "expected_sentiment": "positive",
                        "expected_keywords": [
                            "breast cancer",
                            "immunotherapy",
                            "clinical trials",
                            "treatment",
                        ],
                    },
                    {
                        "title": "Global Breast Cancer Mortality Rates Rise Despite Treatment Advances",
                        "url": "https://medicalresearch.today/mortality-rates-concern-2024",
                        "summary": "Despite significant advances in treatment options, global breast cancer mortality rates have increased by 15% over the past five years, particularly in developing nations with limited healthcare access.",
                        "content": "A comprehensive study published in the International Journal of Oncology reveals troubling trends in global breast cancer mortality. While developed nations have seen improvements in survival rates, developing countries face increasing death rates due to late-stage diagnoses and limited access to modern treatments. The disparity highlights the urgent need for improved healthcare infrastructure and early detection programs worldwide.",
                        "published_at": datetime.now() - timedelta(hours=6),
                        "expected_sentiment": "negative",
                        "expected_keywords": [
                            "breast cancer",
                            "mortality",
                            "developing nations",
                            "healthcare",
                        ],
                    },
                    {
                        "title": "FDA Approves New Diagnostic Imaging Protocol for Early Detection",
                        "url": "https://medicalresearch.today/fda-imaging-approval-2024",
                        "summary": "The FDA has approved a new AI-enhanced mammography protocol that improves early detection accuracy by 25% compared to standard screening methods.",
                        "content": "The Food and Drug Administration announced approval of an advanced AI-enhanced mammography system developed by MedTech Innovations. The system uses machine learning algorithms trained on millions of mammography images to identify subtle patterns indicative of early-stage breast cancer. Clinical trials demonstrated a 25% improvement in detection accuracy and a 30% reduction in false positives compared to traditional mammography.",
                        "published_at": datetime.now() - timedelta(hours=12),
                        "expected_sentiment": "neutral",
                        "expected_keywords": ["FDA", "mammography", "AI", "detection"],
                    },
                ],
            },
            {
                "source": {
                    "name": "International Health Report",
                    "base_url": "https://intlhealth.report",
                    "language": "en",
                    "country": "UK",
                },
                "articles": [
                    {
                        "title": "Preventive Mastectomy Rates Surge Following Celebrity Advocacy",
                        "url": "https://intlhealth.report/preventive-mastectomy-trends",
                        "summary": "Rates of preventive mastectomy procedures have increased significantly following high-profile advocacy campaigns, raising questions about informed consent and medical decision-making.",
                        "content": "Medical professionals report a substantial increase in preventive mastectomy procedures over the past year, largely attributed to celebrity advocacy and increased awareness of genetic testing. While the procedures can be life-saving for high-risk individuals, some experts express concern about whether all patients are receiving adequate genetic counseling and considering all available options.",
                        "published_at": datetime.now() - timedelta(hours=18),
                        "expected_sentiment": "neutral",
                        "expected_keywords": [
                            "preventive mastectomy",
                            "genetic testing",
                            "advocacy",
                        ],
                    },
                    {
                        "title": "Chemotherapy Drug Shortage Creates Treatment Delays Across Europe",
                        "url": "https://intlhealth.report/drug-shortage-crisis",
                        "summary": "A critical shortage of key chemotherapy drugs is forcing treatment delays and protocol modifications across European cancer centers, affecting thousands of breast cancer patients.",
                        "content": "Healthcare systems across Europe are grappling with severe shortages of essential chemotherapy medications, forcing oncologists to delay treatments or modify protocols for breast cancer patients. The shortage, attributed to manufacturing disruptions and supply chain issues, has affected over 15,000 patients continent-wide. Medical professionals are working to implement alternative treatment protocols while advocating for emergency drug imports.",
                        "published_at": datetime.now() - timedelta(hours=24),
                        "expected_sentiment": "negative",
                        "expected_keywords": [
                            "chemotherapy",
                            "drug shortage",
                            "treatment delays",
                            "Europe",
                        ],
                    },
                ],
            },
        ]

    @pytest.mark.asyncio
    async def test_complete_data_pipeline_workflow(
        self, clean_pipeline_environment, sample_news_data
    ):
        """Test complete data pipeline from source creation to analytics"""

        # Phase 1: Source Creation and Configuration
        sources_created = []
        async with clean_pipeline_environment.get_session() as session:
            for source_data in sample_news_data:
                source = NewsSource(
                    name=source_data["source"]["name"],
                    base_url=source_data["source"]["base_url"],
                    language=source_data["source"]["language"],
                    country=source_data["source"]["country"],
                    is_active=True,
                    validation_status="validated",
                )
                session.add(source)
                sources_created.append(source)

            await session.commit()
            for source in sources_created:
                await session.refresh(source)

        # Phase 2: Article Ingestion (Simulating Scraper Output)
        articles_created = []
        for i, source_data in enumerate(sample_news_data):
            source = sources_created[i]
            async with clean_pipeline_environment.get_session() as session:
                for article_data in source_data["articles"]:
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
                for article, _ in articles_created[-len(source_data["articles"]) :]:
                    await session.refresh(article)

        # Phase 3: NLP Processing Pipeline
        sentiment_analyzer = get_sentiment_analyzer()

        for article, expected_data in articles_created:
            # Convert to shared model for NLP
            shared_article = SharedArticle(
                title=article.title,
                published_at=article.published_at,
                summary=article.summary,
                content=article.content,
                url=article.url,
            )

            # Run NLP analysis
            nlp_result = analyze_article(shared_article)

            # Verify NLP results match expectations
            assert nlp_result.is_relevant  # All test articles should be relevant
            assert len(nlp_result.matched_keywords) >= 2  # Should find keywords
            assert nlp_result.sentiment_data["sentiment_label"] in [
                "positive",
                "negative",
                "neutral",
            ]

            # Update database with NLP results
            async with clean_pipeline_environment.get_session() as session:
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
                db_article.word_count = (
                    len(article.content.split()) if article.content else 0
                )

                # Add keywords to database
                for keyword in nlp_result.matched_keywords[:5]:  # Limit to 5 keywords
                    keyword_entry = ArticleKeyword(
                        article_id=article.id,
                        keyword=keyword,
                        relevance_score=0.8,
                        keyword_type="medical_term",
                    )
                    session.add(keyword_entry)

                await session.commit()

        # Phase 4: Data Validation and Quality Checks
        async with clean_pipeline_environment.get_session() as session:
            # Check all articles were processed
            total_articles = await session.execute(select(func.count(Article.id)))
            total_count = total_articles.scalar()
            assert total_count == 5  # We created 5 articles

            # Check all articles have sentiment analysis
            analyzed_articles = await session.execute(
                select(func.count(Article.id)).where(
                    Article.sentiment_label.isnot(None)
                )
            )
            analyzed_count = analyzed_articles.scalar()
            assert analyzed_count == 5  # All should be analyzed

            # Check keyword extraction worked
            total_keywords = await session.execute(
                select(func.count(ArticleKeyword.id))
            )
            keyword_count = total_keywords.scalar()
            assert keyword_count >= 10  # Should have extracted many keywords

            # Verify sentiment distribution
            sentiment_query = await session.execute(
                select(Article.sentiment_label, func.count(Article.id)).group_by(
                    Article.sentiment_label
                )
            )
            sentiment_distribution = dict(sentiment_query.fetchall())

            # Should have both positive and negative sentiments based on test data
            assert sentiment_distribution.get("positive", 0) >= 1
            assert sentiment_distribution.get("negative", 0) >= 1

        # Phase 5: Analytics Generation and Verification
        # Test analytics queries work correctly
        async with clean_pipeline_environment.get_session() as session:
            # Source statistics
            source_stats = await session.execute(
                select(NewsSource.name, func.count(Article.id))
                .join(Article)
                .group_by(NewsSource.name)
            )
            source_counts = dict(source_stats.fetchall())
            assert len(source_counts) == 2  # Two sources
            assert source_counts["Medical Research Today"] == 3
            assert source_counts["International Health Report"] == 2

            # Temporal analysis
            daily_counts = await session.execute(
                select(
                    func.date(Article.published_at).label("date"),
                    func.count(Article.id).label("count"),
                )
                .group_by(func.date(Article.published_at))
                .order_by(func.date(Article.published_at))
            )
            daily_data = daily_counts.fetchall()
            assert len(daily_data) >= 1  # Should have articles from at least one day

            # Geographic distribution
            geo_stats = await session.execute(
                select(Article.country, func.count(Article.id)).group_by(
                    Article.country
                )
            )
            geo_distribution = dict(geo_stats.fetchall())
            assert "US" in geo_distribution
            assert "UK" in geo_distribution

    @pytest.mark.asyncio
    async def test_data_pipeline_error_handling(self, clean_pipeline_environment):
        """Test data pipeline resilience to errors and malformed data"""

        # Test with malformed article data
        async with clean_pipeline_environment.get_session() as session:
            source = NewsSource(
                name="Error Test Source",
                base_url="https://error-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Create articles with problematic data
            problematic_articles = [
                {
                    "title": "",  # Empty title
                    "url": "https://error-test.com/empty-title",
                    "summary": "",  # Empty summary
                    "content": "",  # Empty content
                    "published_at": datetime.now(),
                },
                {
                    "title": "x" * 1000,  # Extremely long title
                    "url": "https://error-test.com/long-title",
                    "summary": "Normal summary",
                    "content": "Normal content",
                    "published_at": datetime.now(),
                },
                {
                    "title": "Special Characters: !@#$%^&*()[]{}|\\:;\"'<>,.?/~`",
                    "url": "https://error-test.com/special-chars",
                    "summary": "Content with unicode: 😀🎉🔬💊",
                    "content": "Mixed content with\nnewlines\tand\ttabs",
                    "published_at": datetime.now(),
                },
            ]

            for article_data in problematic_articles:
                article = Article(
                    source_id=source.id,
                    title=article_data["title"],
                    url=article_data["url"],
                    summary=article_data["summary"],
                    content=article_data["content"],
                    published_at=article_data["published_at"],
                    scraped_at=datetime.now(),
                    processing_status="pending",
                )
                session.add(article)

            await session.commit()

        # Test NLP processing handles problematic data gracefully
        sentiment_analyzer = get_sentiment_analyzer()

        async with clean_pipeline_environment.get_session() as session:
            articles = await session.execute(select(Article))
            for article in articles.scalars():
                shared_article = SharedArticle(
                    title=article.title,
                    published_at=article.published_at,
                    summary=article.summary,
                    content=article.content,
                    url=article.url,
                )

                # NLP should handle errors gracefully
                try:
                    nlp_result = analyze_article(shared_article)
                    # Should not crash, even with problematic data
                    assert nlp_result is not None
                    assert hasattr(nlp_result, "sentiment_data")
                    assert nlp_result.sentiment_data["sentiment_label"] in [
                        "positive",
                        "negative",
                        "neutral",
                    ]
                except Exception as e:
                    pytest.fail(
                        f"NLP processing should handle problematic data gracefully: {e}"
                    )

    @pytest.mark.asyncio
    async def test_data_pipeline_performance_scalability(
        self, clean_pipeline_environment
    ):
        """Test data pipeline performance with larger datasets"""

        # Create moderate-scale test data (100 articles across 10 sources)
        import time

        start_time = time.time()

        # Phase 1: Bulk source creation
        sources = []
        async with clean_pipeline_environment.get_session() as session:
            for i in range(10):
                source = NewsSource(
                    name=f"Performance Test Source {i+1}",
                    base_url=f"https://test-source-{i+1}.com",
                    language="en",
                    country="US",
                    is_active=True,
                    validation_status="validated",
                )
                session.add(source)
                sources.append(source)

            await session.commit()
            for source in sources:
                await session.refresh(source)

        source_creation_time = time.time() - start_time

        # Phase 2: Bulk article creation (10 articles per source)
        article_creation_start = time.time()

        for i, source in enumerate(sources):
            async with clean_pipeline_environment.get_session() as session:
                articles_batch = []
                for j in range(10):
                    article = Article(
                        source_id=source.id,
                        title=f"Performance Test Article {i*10 + j + 1}",
                        url=f"https://test-source-{i+1}.com/article-{j+1}",
                        summary=f"This is performance test article {i*10 + j + 1} for testing data pipeline scalability.",
                        content=f"Detailed content for performance testing article {i*10 + j + 1}. "
                        * 10,
                        published_at=datetime.now() - timedelta(hours=j),
                        scraped_at=datetime.now(),
                        processing_status="pending",
                    )
                    session.add(article)
                    articles_batch.append(article)

                await session.commit()

        article_creation_time = time.time() - article_creation_start

        # Phase 3: Bulk NLP processing
        nlp_processing_start = time.time()

        sentiment_analyzer = get_sentiment_analyzer()

        async with clean_pipeline_environment.get_session() as session:
            articles_query = await session.execute(select(Article))
            articles = list(articles_query.scalars())

            processed_count = 0
            for article in articles:
                shared_article = SharedArticle(
                    title=article.title,
                    published_at=article.published_at,
                    summary=article.summary,
                    content=article.content,
                    url=article.url,
                )

                nlp_result = analyze_article(shared_article)

                # Update article with results (batch update for performance)
                article.sentiment_score = nlp_result.sentiment_data["scores"][
                    "compound"
                ]
                article.sentiment_label = nlp_result.sentiment_data["sentiment_label"]
                article.processing_status = "analyzed"
                processed_count += 1

            await session.commit()

        nlp_processing_time = time.time() - nlp_processing_start
        total_time = time.time() - start_time

        # Performance assertions
        assert (
            source_creation_time < 5.0
        ), f"Source creation took too long: {source_creation_time}s"
        assert (
            article_creation_time < 10.0
        ), f"Article creation took too long: {article_creation_time}s"
        assert (
            nlp_processing_time < 30.0
        ), f"NLP processing took too long: {nlp_processing_time}s"
        assert total_time < 45.0, f"Total pipeline took too long: {total_time}s"

        # Data quality assertions
        async with clean_pipeline_environment.get_session() as session:
            total_articles = await session.execute(select(func.count(Article.id)))
            assert total_articles.scalar() == 100

            analyzed_articles = await session.execute(
                select(func.count(Article.id)).where(
                    Article.sentiment_label.isnot(None)
                )
            )
            assert analyzed_articles.scalar() == 100  # All articles processed

    @pytest.mark.asyncio
    async def test_data_pipeline_concurrent_operations(
        self, clean_pipeline_environment
    ):
        """Test data pipeline behavior under concurrent operations"""

        import concurrent.futures

        # Create base source
        async with clean_pipeline_environment.get_session() as session:
            source = NewsSource(
                name="Concurrent Test Source",
                base_url="https://concurrent-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)
            source_id = source.id

        async def create_article_batch(batch_id: int, count: int):
            """Create a batch of articles concurrently"""
            async with clean_pipeline_environment.get_session() as session:
                for i in range(count):
                    article = Article(
                        source_id=source_id,
                        title=f"Concurrent Article {batch_id}-{i+1}",
                        url=f"https://concurrent-test.com/batch-{batch_id}-article-{i+1}",
                        summary=f"Concurrent test article {batch_id}-{i+1}",
                        content=f"Content for concurrent processing test {batch_id}-{i+1}",
                        published_at=datetime.now() - timedelta(minutes=i),
                        scraped_at=datetime.now(),
                        processing_status="pending",
                    )
                    session.add(article)

                await session.commit()
                return count

        # Create articles concurrently
        tasks = []
        for batch_id in range(5):
            task = create_article_batch(batch_id, 4)  # 5 batches of 4 articles each
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        total_created = sum(results)
        assert total_created == 20  # 5 batches * 4 articles each

        # Verify all articles were created correctly
        async with clean_pipeline_environment.get_session() as session:
            article_count = await session.execute(select(func.count(Article.id)))
            assert article_count.scalar() == 20

            # Verify no duplicate URLs (concurrent inserts handled correctly)
            unique_urls = await session.execute(
                select(func.count(func.distinct(Article.url)))
            )
            assert unique_urls.scalar() == 20  # All URLs should be unique

    @pytest.mark.asyncio
    async def test_data_consistency_across_pipeline_stages(
        self, clean_pipeline_environment, sample_news_data
    ):
        """Test data consistency throughout pipeline stages"""

        # Setup initial data
        async with clean_pipeline_environment.get_session() as session:
            source = NewsSource(
                name="Consistency Test Source",
                base_url="https://consistency-test.com",
                language="en",
                country="US",
                is_active=True,
            )
            session.add(source)
            await session.commit()
            await session.refresh(source)

            # Add articles with known characteristics
            test_articles = [
                {
                    "title": "Positive Medical Breakthrough in Cancer Research",
                    "sentiment": "positive",
                    "keywords": ["cancer", "research", "breakthrough"],
                },
                {
                    "title": "Concerning Rise in Cancer Cases Worldwide",
                    "sentiment": "negative",
                    "keywords": ["cancer", "rise", "concerning"],
                },
                {
                    "title": "FDA Regulatory Update on Medical Devices",
                    "sentiment": "neutral",
                    "keywords": ["FDA", "regulatory", "medical devices"],
                },
            ]

            articles = []
            for i, article_data in enumerate(test_articles):
                article = Article(
                    source_id=source.id,
                    title=article_data["title"],
                    url=f"https://consistency-test.com/article-{i+1}",
                    summary=f"Test summary for {article_data['title']}",
                    content=f"Test content containing {', '.join(article_data['keywords'])}",
                    published_at=datetime.now() - timedelta(hours=i),
                    scraped_at=datetime.now(),
                    processing_status="pending",
                )
                session.add(article)
                articles.append(article)

            await session.commit()
            for article in articles:
                await session.refresh(article)

        # Process with NLP and verify consistency
        sentiment_analyzer = get_sentiment_analyzer()

        for article in articles:
            shared_article = SharedArticle(
                title=article.title,
                published_at=article.published_at,
                summary=article.summary,
                content=article.content,
                url=article.url,
            )

            nlp_result = analyze_article(shared_article)

            async with clean_pipeline_environment.get_session() as session:
                db_article = await session.get(Article, article.id)
                db_article.sentiment_score = nlp_result.sentiment_data["scores"][
                    "compound"
                ]
                db_article.sentiment_label = nlp_result.sentiment_data[
                    "sentiment_label"
                ]
                db_article.processing_status = "analyzed"
                await session.commit()

        # Verify data consistency across different access patterns
        async with clean_pipeline_environment.get_session() as session:
            # Direct database queries
            all_articles = await session.execute(select(Article))
            articles_list = list(all_articles.scalars())

            # Aggregated queries
            sentiment_counts = await session.execute(
                select(Article.sentiment_label, func.count(Article.id)).group_by(
                    Article.sentiment_label
                )
            )
            sentiment_distribution = dict(sentiment_counts.fetchall())

            # Verify consistency
            manual_sentiment_count = {}
            for article in articles_list:
                label = article.sentiment_label
                manual_sentiment_count[label] = manual_sentiment_count.get(label, 0) + 1

            assert sentiment_distribution == manual_sentiment_count
            assert len(articles_list) == 3
            assert all(
                article.processing_status == "analyzed" for article in articles_list
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
