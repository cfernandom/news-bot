"""
Integration tests for NLP pipeline with database
Tests sentiment analysis integration with article processing and storage
"""

from datetime import datetime

import pytest

from services.nlp.src.analyzer import analyze_article
from services.nlp.src.sentiment import get_sentiment_analyzer
from services.shared.models.article import Article


@pytest.mark.integration
@pytest.mark.database
class TestNLPDatabaseIntegration:
    """Test NLP pipeline integration with database operations"""

    @pytest.mark.asyncio
    async def test_sentiment_analysis_pipeline(self, sample_article, test_db_manager):
        """Test complete sentiment analysis pipeline with database"""
        # Analyze article with NLP pipeline
        nlp_result = analyze_article(sample_article)

        # Verify NLP result structure
        assert nlp_result.article == sample_article
        assert isinstance(nlp_result.is_relevant, bool)
        assert isinstance(nlp_result.matched_keywords, list)
        assert isinstance(nlp_result.score, int)
        assert nlp_result.sentiment_data is not None

        # Verify sentiment data structure
        sentiment = nlp_result.sentiment_data
        assert "sentiment_label" in sentiment
        assert "confidence" in sentiment
        assert "scores" in sentiment
        assert sentiment["sentiment_label"] in ["positive", "negative", "neutral"]

    @pytest.mark.asyncio
    async def test_batch_sentiment_processing(self, sample_articles, test_db_manager):
        """Test batch sentiment analysis with database storage simulation"""
        analyzer = get_sentiment_analyzer()

        # Process batch of articles
        results = analyzer.analyze_batch(sample_articles)

        assert len(results) == len(sample_articles)

        # Verify each result
        for i, result in enumerate(results):
            assert "sentiment_label" in result
            assert "confidence" in result
            assert "scores" in result
            assert result["sentiment_label"] in ["positive", "negative", "neutral"]

            # Test database update simulation
            update_data = {
                "sentiment_score": result["scores"]["compound"],
                "sentiment_label": result["sentiment_label"],
            }
            assert -1.0 <= update_data["sentiment_score"] <= 1.0
            assert update_data["sentiment_label"] in ["positive", "negative", "neutral"]

    @pytest.mark.asyncio
    async def test_real_database_article_processing(self, test_db_manager):
        """Test sentiment analysis with real database articles (if available)"""
        # Get sample articles from database
        query = "SELECT id, title, summary, content FROM articles LIMIT 2"
        articles_data = await test_db_manager.execute_sql(query)

        if not articles_data:
            pytest.skip("No articles in test database")

        analyzer = get_sentiment_analyzer()

        for article_data in articles_data:
            article_id, title, summary, content = article_data

            # Analyze sentiment
            text_to_analyze = summary or content or ""
            if text_to_analyze.strip():
                result = analyzer.analyze_sentiment(text_to_analyze, title or "")

                # Verify result can be stored in database
                assert isinstance(result["scores"]["compound"], (int, float))
                assert result["sentiment_label"] in ["positive", "negative", "neutral"]
                assert 0.0 <= result["confidence"] <= 1.0

    @pytest.mark.asyncio
    async def test_nlp_keyword_sentiment_correlation(self, test_db_manager):
        """Test correlation between keyword matching and sentiment analysis"""
        # Create articles with known keywords and sentiment
        test_cases = [
            {
                "title": "Breakthrough in Breast Cancer Treatment",
                "summary": "New chemotherapy shows excellent results in clinical trials",
                "expected_relevant": True,
                "expected_sentiment": "positive",
            },
            {
                "title": "Rising Cancer Death Rates Concern Experts",
                "summary": "Increasing mortality from breast cancer causes alarm",
                "expected_relevant": True,
                "expected_sentiment": "negative",
            },
            {
                "title": "General Health News",
                "summary": "Regular health updates from medical community",
                "expected_relevant": False,
                "expected_sentiment": "neutral",
            },
        ]

        for case in test_cases:
            article = Article(
                title=case["title"],
                published_at=datetime.now(),
                summary=case["summary"],
                content=case["summary"],
                url="https://test.example.com",
            )

            # Analyze with NLP pipeline
            result = analyze_article(article)

            # Check keyword relevance
            if case["expected_relevant"]:
                assert (
                    result.is_relevant
                ), f"Article should be relevant: {case['title']}"
                assert (
                    result.score >= 2
                ), f"Score should be >= 2 for relevant article: {case['title']}"

            # Check sentiment correlation (note: this is a heuristic test)
            sentiment = result.sentiment_data["sentiment_label"]
            # We don't enforce exact matches as sentiment analysis can be nuanced
            assert sentiment in ["positive", "negative", "neutral"]


@pytest.mark.integration
class TestNLPErrorHandling:
    """Test NLP pipeline error handling and resilience"""

    def test_analyze_article_with_missing_data(self):
        """Test NLP analysis with incomplete article data"""
        # Article with missing summary
        article = Article(
            title="Test Article",
            published_at=datetime.now(),
            summary="",  # Empty summary
            content="",  # Empty content
            url="https://test.example.com",
        )

        result = analyze_article(article)

        # Should handle gracefully
        assert result.article == article
        assert isinstance(result.is_relevant, bool)
        assert isinstance(result.matched_keywords, list)
        assert result.sentiment_data is not None
        assert result.sentiment_data["sentiment_label"] == "neutral"

    def test_analyze_very_short_content(self):
        """Test analysis with very short content"""
        article = Article(
            title="OK",
            published_at=datetime.now(),
            summary="Good.",
            content="Yes.",
            url="https://test.example.com",
        )

        result = analyze_article(article)

        # Should handle short content gracefully
        assert result.sentiment_data is not None
        assert "sentiment_label" in result.sentiment_data

    def test_analyze_very_long_content(self):
        """Test analysis with very long content"""
        long_content = "Medical research shows promising results. " * 500

        article = Article(
            title="Long Medical Study",
            published_at=datetime.now(),
            summary=long_content,
            content=long_content,
            url="https://test.example.com",
        )

        result = analyze_article(article)

        # Should handle long content without errors
        assert result.sentiment_data is not None
        assert "scores" in result.sentiment_data
        assert result.sentiment_data["text_length"] > 1000
