"""
Scraper CLI tools for PreventIA News Analytics
Command-line interface for scraper management and automation
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

import click
from sqlalchemy import func, select

from services.data.database.models import Article, NewsSource


# Mock imports for now - these will be implemented later
class ScraperRegistry:
    def has_scraper(self, url):
        return True

    def get_scraper(self, url):
        class MockScraper:
            async def scrape(self):
                return []

        return MockScraper()


class ComplianceValidator:
    async def validate_source(self, url):
        class MockResult:
            is_compliant = True
            violations = []
            robots_txt_compliant = True
            legal_contact_verified = True

        return MockResult()


from .base import BaseCLI, async_command, common_options, validate_source_id


class ScraperCLI(BaseCLI):
    """CLI for scraper management and automation"""

    def __init__(self):
        super().__init__()
        self.scraper_registry = ScraperRegistry()
        self.compliance_validator = ComplianceValidator()

    async def list_sources(self, status_filter: Optional[str] = None) -> List[dict]:
        """List all news sources with scraper information"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource)
            if status_filter:
                query = query.where(NewsSource.status == status_filter)

            result = await session.execute(query)
            sources = result.scalars().all()

            source_data = []
            for source in sources:
                # Get article count
                article_count_query = select(func.count(Article.id)).where(
                    Article.source_id == source.id
                )
                article_result = await session.execute(article_count_query)
                article_count = article_result.scalar() or 0

                # Check if scraper exists
                scraper_exists = self.scraper_registry.has_scraper(source.base_url)

                source_data.append(
                    {
                        "id": source.id,
                        "name": source.name,
                        "base_url": source.base_url,
                        "status": source.status,
                        "scraper_exists": "✅" if scraper_exists else "❌",
                        "articles": article_count,
                        "last_run": (
                            source.last_successful_run.strftime("%Y-%m-%d %H:%M")
                            if source.last_successful_run
                            else "Never"
                        ),
                        "success_rate": (
                            f"{source.success_rate:.1%}"
                            if source.success_rate
                            else "0.0%"
                        ),
                    }
                )

            return source_data

    async def run_scraper(self, source_id: int, force: bool = False) -> dict:
        """Run scraper for a specific source"""
        async with self.db_manager.get_session() as session:
            # Get source
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            source_result = await session.execute(source_query)
            source = source_result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            if source.status != "active" and not force:
                raise click.ClickException(
                    f"Source '{source.name}' is not active. Use --force to override."
                )

            # Check if scraper exists
            if not self.scraper_registry.has_scraper(source.base_url):
                raise click.ClickException(f"No scraper found for {source.base_url}")

            self.log(f"Starting scraper for {source.name} ({source.base_url})")

            # Run compliance check first
            if not force:
                self.log("Running compliance validation...")
                compliance_result = await self.compliance_validator.validate_source(
                    source.base_url
                )
                if not compliance_result.is_compliant:
                    raise click.ClickException(
                        f"Compliance check failed: {', '.join(compliance_result.violations)}"
                    )
                self.log("Compliance validation passed", "success")

            # Get and run scraper
            start_time = datetime.now()
            try:
                scraper = self.scraper_registry.get_scraper(source.base_url)
                articles = await scraper.scrape()

                # Update source statistics
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                source.last_successful_run = end_time
                source.articles_collected_total = (
                    source.articles_collected_total or 0
                ) + len(articles)

                # Calculate success rate (simple approach)
                if source.success_rate is None:
                    source.success_rate = 1.0
                else:
                    source.success_rate = (source.success_rate * 0.9) + (
                        0.1 * 1.0
                    )  # Weighted average

                await session.commit()

                return {
                    "source_id": source_id,
                    "source_name": source.name,
                    "articles_collected": len(articles),
                    "duration_seconds": duration,
                    "success": True,
                    "timestamp": end_time.isoformat(),
                }

            except Exception as e:
                # Update error statistics
                source.error_count_last_30_days = (
                    source.error_count_last_30_days or 0
                ) + 1

                # Decrease success rate
                if source.success_rate is not None:
                    source.success_rate = source.success_rate * 0.9

                await session.commit()

                return {
                    "source_id": source_id,
                    "source_name": source.name,
                    "articles_collected": 0,
                    "duration_seconds": (datetime.now() - start_time).total_seconds(),
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }

    async def run_all_scrapers(
        self, active_only: bool = True, max_concurrent: int = 3
    ) -> List[dict]:
        """Run all scrapers concurrently"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource)
            if active_only:
                query = query.where(NewsSource.status == "active")

            result = await session.execute(query)
            sources = result.scalars().all()

            # Filter sources that have scrapers
            sources_with_scrapers = [
                source
                for source in sources
                if self.scraper_registry.has_scraper(source.base_url)
            ]

            if not sources_with_scrapers:
                self.log("No sources with scrapers found", "warning")
                return []

            self.log(
                f"Running {len(sources_with_scrapers)} scrapers with max {max_concurrent} concurrent"
            )

            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(max_concurrent)

            async def run_single_scraper(source):
                async with semaphore:
                    return await self.run_scraper(source.id, force=False)

            # Run scrapers concurrently
            tasks = [run_single_scraper(source) for source in sources_with_scrapers]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(
                        {
                            "source_id": sources_with_scrapers[i].id,
                            "source_name": sources_with_scrapers[i].name,
                            "success": False,
                            "error": str(result),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                else:
                    processed_results.append(result)

            return processed_results

    async def validate_source_compliance(self, source_id: int) -> dict:
        """Validate compliance for a specific source"""
        async with self.db_manager.get_session() as session:
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            source_result = await session.execute(source_query)
            source = source_result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            self.log(f"Validating compliance for {source.name}")

            compliance_result = await self.compliance_validator.validate_source(
                source.base_url
            )

            # Update source compliance status
            source.robots_txt_compliant = compliance_result.robots_txt_compliant
            source.legal_contact_verified = compliance_result.legal_contact_verified
            source.compliance_last_checked = datetime.now()

            if compliance_result.is_compliant:
                source.risk_level = "low"
            else:
                source.risk_level = (
                    "high" if len(compliance_result.violations) > 2 else "medium"
                )

            await session.commit()

            return {
                "source_id": source_id,
                "source_name": source.name,
                "is_compliant": compliance_result.is_compliant,
                "violations": compliance_result.violations,
                "risk_level": source.risk_level,
                "robots_txt_compliant": compliance_result.robots_txt_compliant,
                "legal_contact_verified": compliance_result.legal_contact_verified,
                "checked_at": datetime.now().isoformat(),
            }

    async def get_scraper_status(self, source_id: Optional[int] = None) -> List[dict]:
        """Get detailed status of scrapers"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource)
            if source_id:
                query = query.where(NewsSource.id == source_id)

            result = await session.execute(query)
            sources = result.scalars().all()

            status_data = []
            for source in sources:
                # Get recent articles
                recent_articles_query = select(func.count(Article.id)).where(
                    Article.source_id == source.id,
                    Article.created_at >= datetime.now() - timedelta(days=7),
                )
                recent_result = await session.execute(recent_articles_query)
                recent_articles = recent_result.scalar() or 0

                # Determine health status
                health_status = "unknown"
                if source.last_successful_run:
                    days_since_run = (datetime.now() - source.last_successful_run).days
                    if days_since_run <= 1:
                        health_status = "healthy"
                    elif days_since_run <= 7:
                        health_status = "warning"
                    else:
                        health_status = "unhealthy"

                status_data.append(
                    {
                        "id": source.id,
                        "name": source.name,
                        "status": source.status,
                        "health": health_status,
                        "scraper_exists": self.scraper_registry.has_scraper(
                            source.base_url
                        ),
                        "compliance": (
                            "compliant"
                            if source.robots_txt_compliant
                            else "non-compliant"
                        ),
                        "articles_last_7_days": recent_articles,
                        "total_articles": source.articles_collected_total or 0,
                        "success_rate": source.success_rate or 0.0,
                        "last_run": (
                            source.last_successful_run.isoformat()
                            if source.last_successful_run
                            else None
                        ),
                        "errors_last_30_days": source.error_count_last_30_days or 0,
                    }
                )

            return status_data


# CLI Commands
@click.group()
@click.pass_context
def scraper(ctx):
    """Scraper management and automation commands"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = ScraperCLI()


@scraper.command()
@click.option(
    "--status",
    type=click.Choice(["active", "inactive", "suspended"]),
    help="Filter by status",
)
@common_options
@click.pass_context
@async_command
async def list(ctx, status, verbose, quiet, format):
    """List all news sources with scraper information"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    sources = await cli.list_sources(status)

    if format == "json":
        click.echo(cli.format_json({"sources": sources}))
    else:
        if not sources:
            cli.log("No sources found", "warning")
            return

        headers = [
            "ID",
            "Name",
            "URL",
            "Status",
            "Scraper",
            "Articles",
            "Last Run",
            "Success Rate",
        ]
        rows = [
            [
                s["id"],
                s["name"][:30],
                s["base_url"][:40],
                s["status"],
                s["scraper_exists"],
                s["articles"],
                s["last_run"],
                s["success_rate"],
            ]
            for s in sources
        ]
        click.echo(cli.format_table(rows, headers))


@scraper.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@click.option("--force", is_flag=True, help="Force run even if source is inactive")
@common_options
@click.pass_context
@async_command
async def run(ctx, source_id, force, verbose, quiet, format):
    """Run scraper for a specific source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.run_scraper(source_id, force)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        if result["success"]:
            cli.log(
                f"Successfully scraped {result['articles_collected']} articles from {result['source_name']}",
                "success",
            )
            cli.log(f"Duration: {result['duration_seconds']:.1f} seconds")
        else:
            cli.log(
                f"Scraper failed for {result['source_name']}: {result.get('error', 'Unknown error')}",
                "error",
            )


@scraper.command()
@click.option(
    "--active-only/--all", default=True, help="Run only active sources or all sources"
)
@click.option(
    "--max-concurrent", type=int, default=3, help="Maximum concurrent scrapers"
)
@common_options
@click.pass_context
@async_command
async def run_all(ctx, active_only, max_concurrent, verbose, quiet, format):
    """Run all scrapers concurrently"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    if not cli.confirm_action(
        f"Run scrapers for {'active' if active_only else 'all'} sources?", True
    ):
        click.echo("Operation cancelled")
        return

    results = await cli.run_all_scrapers(active_only, max_concurrent)

    if format == "json":
        click.echo(cli.format_json({"results": results}))
    else:
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        click.echo(f"\n📊 Scraper Run Summary:")
        click.echo(f"  ✅ Successful: {len(successful)}")
        click.echo(f"  ❌ Failed: {len(failed)}")

        if failed and verbose:
            click.echo("\n❌ Failed scrapers:")
            for result in failed:
                click.echo(
                    f"  - {result['source_name']}: {result.get('error', 'Unknown error')}"
                )


@scraper.command()
@click.argument("source_id", type=int, callback=validate_source_id, required=False)
@common_options
@click.pass_context
@async_command
async def status(ctx, source_id, verbose, quiet, format):
    """Get detailed status of scrapers"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    status_data = await cli.get_scraper_status(source_id)

    if format == "json":
        click.echo(cli.format_json({"status": status_data}))
    else:
        if not status_data:
            cli.log("No sources found", "warning")
            return

        headers = [
            "ID",
            "Name",
            "Status",
            "Health",
            "Compliance",
            "Articles (7d)",
            "Success Rate",
        ]
        rows = [
            [
                s["id"],
                s["name"][:25],
                s["status"],
                s["health"],
                s["compliance"],
                s["articles_last_7_days"],
                f"{s['success_rate']:.1%}",
            ]
            for s in status_data
        ]
        click.echo(cli.format_table(rows, headers))


@scraper.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@common_options
@click.pass_context
@async_command
async def validate(ctx, source_id, verbose, quiet, format):
    """Validate compliance for a specific source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.validate_source_compliance(source_id)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        if result["is_compliant"]:
            cli.log(f"Source '{result['source_name']}' is compliant", "success")
        else:
            cli.log(
                f"Source '{result['source_name']}' has compliance violations:",
                "warning",
            )
            for violation in result["violations"]:
                cli.log(f"  - {violation}", "warning")

        cli.log(f"Risk level: {result['risk_level']}")


if __name__ == "__main__":
    scraper()
