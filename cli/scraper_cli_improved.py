"""
Improved scraper management CLI tools for PreventIA News Analytics
Command-line interface for scraper administration and registry management
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import click
from tabulate import tabulate

from services.scraper.src.registry import get_scraper_registry

from .base import BaseCLI, async_command, common_options

logger = logging.getLogger(__name__)


class ScraperCLI(BaseCLI):
    """CLI for scraper management and registry operations"""

    def __init__(self):
        super().__init__()
        self.registry = get_scraper_registry()

    def format_scraper_table(self, scrapers: List[Dict]) -> str:
        """Format scrapers data as a table"""
        headers = [
            "Domain",
            "Name",
            "Type",
            "Priority",
            "Active",
            "Success Rate",
            "Last Used",
        ]
        rows = []

        for scraper in scrapers:
            last_used = scraper.get("last_used", "Never")
            if last_used and last_used != "Never":
                try:
                    last_used = datetime.fromisoformat(last_used.replace("Z", "+00:00"))
                    last_used = last_used.strftime("%Y-%m-%d %H:%M")
                except:
                    last_used = str(last_used)[:16]

            rows.append(
                [
                    scraper["domain"],
                    scraper["name"][:20],
                    scraper["type"],
                    scraper["priority"],
                    "✅" if scraper["active"] else "❌",
                    f"{scraper['success_rate']:.1%}",
                    last_used,
                ]
            )

        return tabulate(rows, headers=headers, tablefmt="grid")

    async def list_scrapers(
        self, domain_filter: Optional[str] = None, active_only: bool = False
    ) -> List[Dict]:
        """List all scrapers or scrapers for a specific domain"""
        if domain_filter:
            scrapers = self.registry.get_scrapers_for_domain(domain_filter)
        else:
            scrapers = self.registry.get_all_active_scrapers() if active_only else []
            if not active_only:
                # Get all scrapers from all domains
                scrapers = []
                for domain in self.registry._scrapers:
                    scrapers.extend(self.registry.get_scrapers_for_domain(domain))

        return [
            {
                "domain": s.domain,
                "name": s.name,
                "type": s.scraper_type.value,
                "priority": s.priority,
                "active": s.is_active,
                "success_rate": s.success_rate,
                "last_used": s.last_used.isoformat() if s.last_used else None,
                "description": s.description,
            }
            for s in scrapers
        ]

    async def run_all_scrapers(self) -> Dict:
        """Run all primary scrapers using the registry system"""
        from services.scraper.src.main import scrape_articles

        try:
            articles = await scrape_articles()

            return {
                "success": True,
                "total_articles": len(articles),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }


# CLI Commands
@click.group()
@click.pass_context
def scraper(ctx):
    """Scraper management and automation commands"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = ScraperCLI()


@scraper.command()
@click.option("--domain", help="Filter by domain")
@click.option("--active-only", is_flag=True, help="Show only active scrapers")
@common_options
@click.pass_context
@async_command
async def list(ctx, domain, active_only, verbose, quiet, format):
    """List all scrapers"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    scrapers = await cli.list_scrapers(domain, active_only)

    if format == "json":
        click.echo(cli.format_json({"scrapers": scrapers}))
    else:
        if not scrapers:
            cli.log("No scrapers found", "warning")
            return

        click.echo(cli.format_scraper_table(scrapers))


@scraper.command()
@common_options
@click.pass_context
@async_command
async def run_all(ctx, verbose, quiet, format):
    """Run all primary scrapers"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    click.echo("🚀 Running all primary scrapers...")

    result = await cli.run_all_scrapers()

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        if result["success"]:
            click.echo(f"✅ All scrapers completed")
            click.echo(f"  Total Articles: {result['total_articles']}")
            click.echo(f"  Timestamp: {result['timestamp']}")
        else:
            click.echo(f"❌ Scraper execution failed: {result['error']}")


@scraper.command()
@common_options
@click.pass_context
@async_command
async def status(ctx, verbose, quiet, format):
    """Show scraper registry status"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.registry.get_registry_status()

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"\n📊 Registry Status:")
        click.echo(f"  Total Scrapers: {result['total_scrapers']}")
        click.echo(f"  Active Scrapers: {result['active_scrapers']}")
        click.echo(f"  Primary Scrapers: {result['primary_scrapers']}")
        click.echo(f"  Domains Covered: {result['domains_covered']}")
        click.echo(f"  Domains Active: {result['domains_active']}")
        click.echo(f"  Registry Health: {result['registry_health']:.1%}")


if __name__ == "__main__":
    scraper()
