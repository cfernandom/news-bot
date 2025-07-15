import asyncio
import importlib
from datetime import datetime
from typing import List

from services.scraper.src.cache_manager import get_cache_manager
from services.scraper.src.performance_monitor import (
    PerformanceTracker,
    get_performance_monitor,
)
from services.scraper.src.rate_limiter import RateLimitedRequest, get_rate_limiter
from services.scraper.src.registry import get_scraper_registry
from services.scraper.src.scraper_config import get_scraper_config
from services.shared.logging.structured_logger import get_logger
from services.shared.models.article import Article

logger = get_logger("scraper")


async def scrape_single_domain(
    scraper_info, registry, rate_limiter, cache_manager, performance_monitor
) -> List[Article]:
    """
    Scrape a single domain with performance optimization and monitoring
    """
    articles = []
    domain = scraper_info.domain
    scraper_name = scraper_info.name

    # Get domain-specific configuration
    config = get_scraper_config(domain)

    # Start performance tracking
    with PerformanceTracker(domain, scraper_name) as tracker:
        try:
            # Check rate limiting
            async with RateLimitedRequest(domain, "scrape_articles"):
                logger.scraper_started(domain, scraper_name)

                # Check cache first if enabled
                if config.enable_caching:
                    cache_key = f"scraper_run_{domain}_{scraper_name}"
                    cached_result = cache_manager.get_cached_article(cache_key, domain)

                    if cached_result:
                        logger.info(
                            "Using cached scraper results",
                            domain=domain,
                            scraper_name=scraper_name,
                            cached_articles=len(cached_result.get("articles", [])),
                        )
                        return cached_result.get("articles", [])

                # Dynamically import the scraper function
                module = importlib.import_module(scraper_info.module_path)
                scraper_func = getattr(module, scraper_info.function_name)

                # Execute the scraper with timeout
                try:
                    result = await asyncio.wait_for(
                        scraper_func(), timeout=config.timeout_seconds
                    )
                except asyncio.TimeoutError:
                    raise Exception(
                        f"Scraper timeout after {config.timeout_seconds} seconds"
                    )

                if result:
                    # Filter articles based on configuration
                    filtered_articles = []

                    for article in result[: config.max_articles_per_run]:
                        # Check content length
                        if len(article.content or "") < config.min_content_length:
                            continue
                        if len(article.content or "") > config.max_content_length:
                            continue

                        # Check title length
                        if len(article.title or "") < config.min_title_length:
                            continue
                        if len(article.title or "") > config.max_title_length:
                            continue

                        # Check if date is required
                        if config.date_required and not article.published_at:
                            continue

                        # Check if summary is required
                        if config.require_summary and not article.summary:
                            continue
                        if (
                            config.require_summary
                            and len(article.summary or "") < config.min_summary_length
                        ):
                            continue

                        # Check for duplicates if enabled
                        if config.skip_duplicates:
                            if cache_manager.is_article_cached(article.url, domain):
                                tracker.record_article_quality(
                                    has_date=bool(article.published_at),
                                    has_summary=bool(article.summary),
                                    is_duplicate=True,
                                )
                                continue

                        # Record article quality metrics
                        tracker.record_article_quality(
                            has_date=bool(article.published_at),
                            has_summary=bool(article.summary),
                            is_duplicate=False,
                        )

                        # Cache the article if enabled
                        if config.enable_caching:
                            cache_manager.cache_article(
                                article.url,
                                domain,
                                article.content or "",
                                {
                                    "title": article.title,
                                    "summary": article.summary,
                                    "published_at": (
                                        article.published_at.isoformat()
                                        if article.published_at
                                        else None
                                    ),
                                },
                            )

                        filtered_articles.append(article)

                    articles = filtered_articles
                    tracker.set_articles_found(len(articles))

                    # Cache the scraper run result if enabled
                    if config.enable_caching:
                        cache_manager.cache_scraper_run(
                            domain,
                            scraper_name,
                            len(articles),
                            0.0,  # execution time will be calculated by tracker
                            True,
                        )

                    logger.scraper_completed(
                        domain,
                        scraper_name,
                        len(articles),
                        0.0,  # execution time will be calculated by tracker
                    )

                    # Update success stats
                    registry.update_scraper_stats(
                        domain, scraper_name, success=True, last_used=datetime.now()
                    )

                else:
                    logger.warning(
                        "No articles returned", domain=domain, scraper_name=scraper_name
                    )

                    # Update stats for empty result
                    registry.update_scraper_stats(
                        domain,
                        scraper_name,
                        success=True,  # Empty result is still success
                        last_used=datetime.now(),
                    )

        except Exception as e:
            logger.scraper_failed(domain, scraper_name, str(e))

            # Update failure stats
            registry.update_scraper_stats(
                domain, scraper_name, success=False, last_used=datetime.now()
            )

            # Try fallback scrapers
            fallback_scrapers = registry.get_fallback_scrapers(domain)
            if fallback_scrapers:
                logger.info(
                    "Trying fallback scrapers",
                    domain=domain,
                    fallback_count=len(fallback_scrapers),
                )

                for fallback in fallback_scrapers:
                    try:
                        logger.info(
                            "Trying fallback scraper",
                            domain=fallback.domain,
                            scraper_name=fallback.name,
                        )

                        fallback_module = importlib.import_module(fallback.module_path)
                        fallback_func = getattr(fallback_module, fallback.function_name)

                        result = await fallback_func()
                        if result:
                            articles = result[: config.max_articles_per_run]
                            tracker.set_articles_found(len(articles))

                            logger.scraper_completed(
                                fallback.domain,
                                fallback.name,
                                len(articles),
                                0.0,  # Don't track execution time for fallback
                                fallback=True,
                            )

                            registry.update_scraper_stats(
                                fallback.domain,
                                fallback.name,
                                success=True,
                                last_used=datetime.now(),
                            )
                            break

                    except Exception as fallback_error:
                        logger.scraper_failed(
                            fallback.domain, fallback.name, str(fallback_error)
                        )
                        registry.update_scraper_stats(
                            fallback.domain,
                            fallback.name,
                            success=False,
                            last_used=datetime.now(),
                        )
                        continue

    return articles


async def scrape_articles() -> List[Article]:
    """
    Scrape articles using the optimized concurrent system with rate limiting and caching.
    """
    registry = get_scraper_registry()
    rate_limiter = get_rate_limiter()
    cache_manager = get_cache_manager()
    performance_monitor = get_performance_monitor()

    # Get all primary scrapers (one per domain)
    primary_scrapers = registry.get_all_primary_scrapers()

    logger.info(
        "Starting optimized scraper execution", total_scrapers=len(primary_scrapers)
    )

    # Create semaphore for concurrent execution
    max_concurrent = min(len(primary_scrapers), 5)  # Limit concurrent scrapers
    semaphore = asyncio.Semaphore(max_concurrent)

    async def scrape_with_semaphore(scraper_info):
        async with semaphore:
            return await scrape_single_domain(
                scraper_info, registry, rate_limiter, cache_manager, performance_monitor
            )

    # Execute scrapers concurrently
    tasks = [scrape_with_semaphore(scraper_info) for scraper_info in primary_scrapers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Collect all articles from successful results
    all_articles = []
    success_count = 0
    error_count = 0

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            error_count += 1
            logger.error(
                "Scraper task failed",
                domain=primary_scrapers[i].domain,
                scraper_name=primary_scrapers[i].name,
                error=str(result),
            )
        else:
            success_count += 1
            all_articles.extend(result)

    # Log final statistics
    logger.info(
        "Scraper execution completed",
        total_articles=len(all_articles),
        successful_scrapers=success_count,
        failed_scrapers=error_count,
        success_rate=success_count / len(primary_scrapers) if primary_scrapers else 0,
    )

    # Clean up old cache entries
    cache_manager.cleanup_expired_entries()

    # Clean up old performance metrics
    performance_monitor.cleanup_old_metrics()

    return all_articles
