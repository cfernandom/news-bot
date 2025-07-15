"""
Unified scraper system for PreventIA News Analytics
Combines the best of both regular and PostgreSQL scrapers
"""

import asyncio
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from sqlalchemy import select

from services.data.database.connection import db_manager
from services.data.database.models import Article as ArticleModel
from services.data.database.models import NewsSource
from services.scraper.src.scraper_config import get_scraper_config
from services.shared.config import settings
from services.shared.exceptions import (
    DatabaseException,
    ErrorContext,
    ScraperException,
    error_handler,
    handle_database_error,
    handle_scraper_error,
)
from services.shared.logging.structured_logger import get_logger
from services.shared.models.article import Article

logger = get_logger("scraper.unified")


@dataclass
class ScraperResult:
    """Unified scraper result with metadata"""

    articles: List[Article]
    saved_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    execution_time: float = 0.0
    source_id: Optional[int] = None
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class UnifiedScraper:
    """
    Unified scraper that can operate in different modes:
    1. Memory-only: Returns Article objects (like regular scrapers)
    2. Database-direct: Saves directly to database (like PostgreSQL scrapers)
    3. Hybrid: Returns articles AND saves to database
    """

    def __init__(self, domain: str):
        self.domain = domain
        self.config = get_scraper_config(domain)
        self.logger = get_logger(f"scraper.unified.{domain}")

    @error_handler(exceptions=Exception, reraise=False)
    async def execute_scraper(
        self,
        scraper_function: callable,
        mode: str = "hybrid",  # "memory", "database", "hybrid"
        auto_create_source: bool = True,
    ) -> ScraperResult:
        """
        Execute a scraper function in the specified mode

        Args:
            scraper_function: The actual scraper function to execute
            mode: "memory", "database", or "hybrid"
            auto_create_source: Whether to create missing news sources

        Returns:
            ScraperResult with articles and metadata
        """
        start_time = asyncio.get_event_loop().time()
        result = ScraperResult(articles=[], source_id=None)

        with ErrorContext(
            f"scraper_execution_{self.domain}", {"mode": mode, "domain": self.domain}
        ):
            try:
                # Execute the actual scraper function
                self.logger.info(f"Executing scraper for {self.domain} in {mode} mode")
                articles = await scraper_function()

                if not articles:
                    self.logger.warning(f"No articles returned from {self.domain}")
                    return result

                # Filter articles based on configuration
                filtered_articles = await self._filter_articles(articles)
                result.articles = filtered_articles
                result.skipped_count = len(articles) - len(filtered_articles)

                # Handle database operations based on mode
                if mode in ["database", "hybrid"]:
                    source_id = await self._ensure_news_source(auto_create_source)
                    if source_id:
                        result.source_id = source_id
                        saved_count = await self._save_articles_to_database(
                            filtered_articles, source_id
                        )
                        result.saved_count = saved_count
                    else:
                        raise ScraperException(
                            domain=self.domain,
                            scraper_name="unified",
                            message="Could not find or create news source",
                            details={"auto_create": auto_create_source},
                        )

                # Calculate execution time
                result.execution_time = asyncio.get_event_loop().time() - start_time

                self.logger.info(
                    f"Scraper completed",
                    domain=self.domain,
                    mode=mode,
                    total_found=len(articles),
                    filtered=len(filtered_articles),
                    saved=result.saved_count,
                    execution_time=result.execution_time,
                )

                return result

            except ScraperException:
                # Re-raise our custom exceptions
                raise
            except Exception as e:
                # Convert to ScraperException for consistency
                raise ScraperException(
                    domain=self.domain,
                    scraper_name="unified",
                    message=str(e),
                    original_exception=e,
                )

    async def _filter_articles(self, articles: List[Article]) -> List[Article]:
        """Filter articles based on configuration requirements"""
        filtered = []

        for article in articles:
            # Check title requirements
            if not article.title or len(article.title) < self.config.min_title_length:
                continue
            if len(article.title) > self.config.max_title_length:
                continue

            # Check date requirements
            if self.config.date_required and not article.published_at:
                continue

            # Check summary requirements
            if self.config.require_summary:
                if not article.summary:
                    continue
                if len(article.summary) < self.config.min_summary_length:
                    continue

            # Check content length (usually 0 for metadata-only)
            if (
                article.content
                and len(article.content) < self.config.min_content_length
            ):
                continue
            if (
                article.content
                and len(article.content) > self.config.max_content_length
            ):
                continue

            filtered.append(article)

        return filtered

    async def _ensure_news_source(self, auto_create: bool = True) -> Optional[int]:
        """Ensure news source exists, create if necessary"""
        try:
            await db_manager.initialize()

            async with db_manager.get_session() as session:
                # Try to find existing source
                parsed_url = urlparse(f"https://{self.domain}")
                domain_variations = [
                    f"https://{self.domain}/",
                    f"https://{self.domain}",
                    f"https://www.{self.domain.replace('www.', '')}/",
                    f"https://www.{self.domain.replace('www.', '')}",
                ]

                for url_variant in domain_variations:
                    result = await session.execute(
                        select(NewsSource).where(NewsSource.base_url == url_variant)
                    )
                    source = result.scalar_one_or_none()
                    if source:
                        return source.id

                # Create new source if auto_create is enabled
                if auto_create:
                    source_name = (
                        self.domain.replace("www.", "")
                        .replace(".com", "")
                        .replace(".org", "")
                        .replace(".net", "")
                        .title()
                    )

                    new_source = NewsSource(
                        name=source_name,
                        base_url=f"https://{self.domain}/",
                        language="en",
                        country="US",
                        is_active=True,
                        validation_status="pending",
                    )

                    session.add(new_source)
                    await session.flush()
                    await session.commit()

                    self.logger.info(
                        f"Created new news source: {source_name} ({new_source.id})"
                    )
                    return new_source.id

                return None

        except Exception as e:
            self.logger.error(f"Error ensuring news source for {self.domain}: {e}")
            return None

    async def _save_articles_to_database(
        self, articles: List[Article], source_id: int
    ) -> int:
        """Save articles to database with duplicate detection"""
        saved_count = 0

        try:
            async with db_manager.get_session() as session:
                for article in articles:
                    try:
                        # Check for duplicates
                        existing = await session.execute(
                            select(ArticleModel).where(ArticleModel.url == article.url)
                        )
                        if existing.scalar_one_or_none():
                            continue

                        # Generate content hash
                        content_hash = hashlib.sha256(
                            (
                                article.title + article.url + (article.content or "")
                            ).encode("utf-8")
                        ).hexdigest()

                        # Handle timezone-naive datetime
                        published_at = article.published_at
                        if published_at and published_at.tzinfo:
                            published_at = published_at.replace(tzinfo=None)

                        # Create database article
                        db_article = ArticleModel(
                            source_id=source_id,
                            title=article.title,
                            url=article.url,
                            content=article.content or "",
                            summary=article.summary or "",
                            published_at=published_at,
                            content_hash=content_hash,
                            word_count=(
                                len(article.content.split()) if article.content else 0
                            ),
                            processing_status="pending",
                            language="en",
                            country="US",
                        )

                        session.add(db_article)
                        saved_count += 1

                    except Exception as e:
                        self.logger.error(f"Error saving article {article.title}: {e}")
                        continue

                await session.commit()

        except Exception as e:
            self.logger.error(f"Error saving articles to database: {e}")

        return saved_count

    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for this scraper"""
        try:
            await db_manager.initialize()

            # Get recent performance data
            async with db_manager.get_connection() as conn:
                query = """
                SELECT
                    COUNT(*) as total_articles,
                    COUNT(CASE WHEN created_at > NOW() - INTERVAL '24 hours' THEN 1 END) as recent_articles,
                    AVG(word_count) as avg_word_count,
                    COUNT(CASE WHEN published_at IS NOT NULL THEN 1 END) as articles_with_dates,
                    COUNT(CASE WHEN summary IS NOT NULL AND length(summary) > 0 THEN 1 END) as articles_with_summaries
                FROM articles a
                JOIN news_sources ns ON a.source_id = ns.id
                WHERE ns.base_url LIKE %s
                """

                result = await conn.fetchrow(query, f"%{self.domain}%")

                if result:
                    return {
                        "domain": self.domain,
                        "total_articles": result["total_articles"],
                        "recent_articles": result["recent_articles"],
                        "avg_word_count": float(result["avg_word_count"] or 0),
                        "articles_with_dates": result["articles_with_dates"],
                        "articles_with_summaries": result["articles_with_summaries"],
                        "date_completion_rate": result["articles_with_dates"]
                        / max(result["total_articles"], 1),
                        "summary_completion_rate": result["articles_with_summaries"]
                        / max(result["total_articles"], 1),
                    }

        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {e}")

        return {"domain": self.domain, "error": "Could not fetch metrics"}


# Helper functions for backward compatibility
async def execute_scraper_unified(
    domain: str, scraper_function: callable, mode: str = "hybrid"
) -> ScraperResult:
    """
    Execute a scraper function using the unified system

    Args:
        domain: Domain name (e.g., "breastcancer.org")
        scraper_function: The scraper function to execute
        mode: "memory", "database", or "hybrid"

    Returns:
        ScraperResult with articles and metadata
    """
    unified_scraper = UnifiedScraper(domain)
    return await unified_scraper.execute_scraper(scraper_function, mode)


# Factory function to create scrapers
def create_unified_scraper(domain: str) -> UnifiedScraper:
    """Create a unified scraper for a domain"""
    return UnifiedScraper(domain)


if __name__ == "__main__":
    # Example usage
    async def test_unified_scraper():
        """Test the unified scraper system"""

        # Example with a simple scraper function
        async def dummy_scraper():
            return [
                Article(
                    title="Test Article 1",
                    url="https://example.com/article1",
                    summary="This is a test summary that meets the minimum length requirement.",
                    published_at=datetime.now(),
                    content="",
                )
            ]

        # Test in different modes
        scraper = UnifiedScraper("example.com")

        print("Testing memory mode...")
        result_memory = await scraper.execute_scraper(dummy_scraper, mode="memory")
        print(
            f"Memory mode: {len(result_memory.articles)} articles, {result_memory.saved_count} saved"
        )

        print("Testing hybrid mode...")
        result_hybrid = await scraper.execute_scraper(dummy_scraper, mode="hybrid")
        print(
            f"Hybrid mode: {len(result_hybrid.articles)} articles, {result_hybrid.saved_count} saved"
        )

        print("Getting performance metrics...")
        metrics = await scraper.get_performance_metrics()
        print(f"Metrics: {metrics}")

    asyncio.run(test_unified_scraper())
