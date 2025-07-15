"""
Scraper adapter for migrating existing scrapers to unified system
Provides backward compatibility while enabling new features
"""

import asyncio
import importlib
from typing import Any, Callable, Dict, List, Optional

from services.scraper.src.registry import ScraperInfo, ScraperType, get_scraper_registry
from services.scraper.src.unified_scraper import ScraperResult, UnifiedScraper
from services.shared.exceptions import (
    ErrorContext,
    ScraperException,
    error_handler,
    handle_scraper_error,
)
from services.shared.logging.structured_logger import get_logger
from services.shared.models.article import Article

logger = get_logger("scraper.adapter")


class ScraperAdapter:
    """
    Adapter to migrate existing scrapers to the unified system
    Provides smooth transition while maintaining backward compatibility
    """

    def __init__(self):
        self.registry = get_scraper_registry()
        self.unified_scrapers: Dict[str, UnifiedScraper] = {}

    def get_unified_scraper(self, domain: str) -> UnifiedScraper:
        """Get or create a unified scraper for a domain"""
        if domain not in self.unified_scrapers:
            self.unified_scrapers[domain] = UnifiedScraper(domain)
        return self.unified_scrapers[domain]

    @error_handler(exceptions=Exception, reraise=False)
    async def execute_legacy_scraper(
        self, scraper_info: ScraperInfo, mode: str = "hybrid"
    ) -> ScraperResult:
        """
        Execute a legacy scraper using the unified system

        Args:
            scraper_info: Scraper information from registry
            mode: "memory", "database", or "hybrid"

        Returns:
            ScraperResult with articles and metadata
        """
        with ErrorContext(
            f"legacy_scraper_execution",
            {
                "scraper_name": scraper_info.name,
                "domain": scraper_info.domain,
                "mode": mode,
            },
        ):
            try:
                # Import the scraper module dynamically
                module = importlib.import_module(scraper_info.module_path)
                scraper_function = getattr(module, scraper_info.function_name)

                # Get unified scraper for this domain
                unified_scraper = self.get_unified_scraper(scraper_info.domain)

                # Execute using unified system
                result = await unified_scraper.execute_scraper(
                    scraper_function=scraper_function,
                    mode=mode,
                    auto_create_source=True,
                )

                logger.info(
                    f"Executed legacy scraper via adapter",
                    scraper_name=scraper_info.name,
                    domain=scraper_info.domain,
                    mode=mode,
                    articles_found=len(result.articles),
                    articles_saved=result.saved_count,
                )

                return result

            except ScraperException:
                # Re-raise our custom exceptions
                raise
            except Exception as e:
                # Convert to ScraperException for consistency
                raise ScraperException(
                    domain=scraper_info.domain,
                    scraper_name=scraper_info.name,
                    message=str(e),
                    original_exception=e,
                    details={"adapter": "legacy", "mode": mode},
                )

    async def execute_all_active_scrapers(
        self, mode: str = "hybrid", max_concurrent: int = 5
    ) -> Dict[str, ScraperResult]:
        """
        Execute all active scrapers using the unified system

        Args:
            mode: "memory", "database", or "hybrid"
            max_concurrent: Maximum concurrent scrapers

        Returns:
            Dictionary mapping domain to ScraperResult
        """
        # Get all primary active scrapers
        primary_scrapers = self.registry.get_all_primary_scrapers()

        logger.info(f"Executing {len(primary_scrapers)} active scrapers in {mode} mode")

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(scraper_info: ScraperInfo) -> tuple:
            async with semaphore:
                result = await self.execute_legacy_scraper(scraper_info, mode)
                return scraper_info.domain, result

        # Execute all scrapers concurrently
        tasks = [
            execute_with_semaphore(scraper_info) for scraper_info in primary_scrapers
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        domain_results = {}
        successful_count = 0
        error_count = 0
        total_articles = 0

        for result in results:
            if isinstance(result, Exception):
                error_count += 1
                logger.error(f"Scraper task failed: {result}")
            else:
                domain, scraper_result = result
                domain_results[domain] = scraper_result

                if scraper_result.error_count == 0:
                    successful_count += 1
                    total_articles += len(scraper_result.articles)
                else:
                    error_count += 1

        logger.info(
            f"Completed scraper execution",
            mode=mode,
            total_scrapers=len(primary_scrapers),
            successful=successful_count,
            failed=error_count,
            total_articles=total_articles,
        )

        return domain_results

    async def migrate_scraper_to_unified(
        self, domain: str, test_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Migrate a specific scraper to unified system and compare results

        Args:
            domain: Domain to migrate
            test_mode: If True, compares old vs new without saving

        Returns:
            Migration report with comparison results
        """
        migration_report = {
            "domain": domain,
            "status": "unknown",
            "old_result": None,
            "new_result": None,
            "comparison": None,
            "recommendation": None,
        }

        try:
            # Get scraper info for this domain
            scraper_info = self.registry.get_primary_scraper(domain)
            if not scraper_info:
                migration_report["status"] = "error"
                migration_report["recommendation"] = (
                    f"No primary scraper found for {domain}"
                )
                return migration_report

            # Execute old scraper (memory mode)
            logger.info(f"Testing legacy scraper for {domain}")
            old_result = await self.execute_legacy_scraper(scraper_info, mode="memory")
            migration_report["old_result"] = {
                "articles_count": len(old_result.articles),
                "execution_time": old_result.execution_time,
                "errors": old_result.errors,
            }

            # Execute new unified scraper
            logger.info(f"Testing unified scraper for {domain}")
            mode = "memory" if test_mode else "hybrid"
            new_result = await self.execute_legacy_scraper(scraper_info, mode=mode)
            migration_report["new_result"] = {
                "articles_count": len(new_result.articles),
                "saved_count": new_result.saved_count,
                "execution_time": new_result.execution_time,
                "errors": new_result.errors,
            }

            # Compare results
            articles_match = len(old_result.articles) == len(new_result.articles)
            both_successful = (
                old_result.error_count == 0 and new_result.error_count == 0
            )
            performance_improvement = (
                old_result.execution_time > new_result.execution_time
                if both_successful
                else False
            )

            migration_report["comparison"] = {
                "articles_match": articles_match,
                "both_successful": both_successful,
                "performance_improvement": performance_improvement,
                "time_difference": new_result.execution_time
                - old_result.execution_time,
            }

            # Generate recommendation
            if both_successful and articles_match:
                migration_report["status"] = "success"
                migration_report["recommendation"] = (
                    "Safe to migrate - results are consistent"
                )
            elif both_successful and not articles_match:
                migration_report["status"] = "warning"
                migration_report["recommendation"] = (
                    f"Article count differs: old={len(old_result.articles)}, new={len(new_result.articles)}. Investigate differences."
                )
            else:
                migration_report["status"] = "error"
                migration_report["recommendation"] = (
                    "Migration not recommended - errors detected"
                )

            logger.info(
                f"Migration test completed for {domain}",
                status=migration_report["status"],
                recommendation=migration_report["recommendation"],
            )

        except Exception as e:
            migration_report["status"] = "error"
            migration_report["recommendation"] = f"Migration test failed: {str(e)}"
            logger.error(f"Migration test failed for {domain}: {e}")

        return migration_report

    async def get_migration_report_all_domains(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate migration report for all domains

        Returns:
            Dictionary mapping domain to migration report
        """
        primary_scrapers = self.registry.get_all_primary_scrapers()
        domains = [scraper_info.domain for scraper_info in primary_scrapers]

        logger.info(f"Generating migration report for {len(domains)} domains")

        migration_reports = {}
        for domain in domains:
            report = await self.migrate_scraper_to_unified(domain, test_mode=True)
            migration_reports[domain] = report

        # Generate summary
        successful = sum(
            1 for report in migration_reports.values() if report["status"] == "success"
        )
        warnings = sum(
            1 for report in migration_reports.values() if report["status"] == "warning"
        )
        errors = sum(
            1 for report in migration_reports.values() if report["status"] == "error"
        )

        logger.info(
            f"Migration report completed",
            total_domains=len(domains),
            successful=successful,
            warnings=warnings,
            errors=errors,
        )

        return migration_reports


# Global adapter instance
_adapter = ScraperAdapter()


def get_scraper_adapter() -> ScraperAdapter:
    """Get the global scraper adapter instance"""
    return _adapter


# Convenience functions
async def execute_domain_unified(domain: str, mode: str = "hybrid") -> ScraperResult:
    """Execute a domain's scraper using the unified system"""
    adapter = get_scraper_adapter()
    registry = get_scraper_registry()

    scraper_info = registry.get_primary_scraper(domain)
    if not scraper_info:
        return ScraperResult(
            articles=[],
            error_count=1,
            errors=[f"No primary scraper found for domain: {domain}"],
        )

    return await adapter.execute_legacy_scraper(scraper_info, mode)


async def execute_all_domains_unified(mode: str = "hybrid") -> Dict[str, ScraperResult]:
    """Execute all domains using the unified system"""
    adapter = get_scraper_adapter()
    return await adapter.execute_all_active_scrapers(mode)


if __name__ == "__main__":
    # Example usage
    async def test_adapter():
        """Test the scraper adapter"""
        adapter = get_scraper_adapter()

        # Test a specific domain
        print("Testing specific domain migration...")
        domain = "breastcancer.org"
        report = await adapter.migrate_scraper_to_unified(domain, test_mode=True)
        print(f"Migration report for {domain}: {report}")

        # Test all domains
        print("\\nTesting all domains...")
        results = await adapter.execute_all_active_scrapers(
            mode="memory", max_concurrent=3
        )

        total_articles = sum(len(result.articles) for result in results.values())
        successful_domains = sum(
            1 for result in results.values() if result.error_count == 0
        )

        print(
            f"Results: {len(results)} domains, {successful_domains} successful, {total_articles} total articles"
        )

        for domain, result in results.items():
            status = "✅" if result.error_count == 0 else "❌"
            print(f"  {status} {domain}: {len(result.articles)} articles")

    asyncio.run(test_adapter())
