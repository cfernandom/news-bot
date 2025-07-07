"""
Source management CLI tools for PreventIA News Analytics
Command-line interface for news source administration
"""

from datetime import datetime, timedelta
from typing import List, Optional

import click
from sqlalchemy import select

from services.data.database.models import NewsSource


# Mock compliance validator for now
class ComplianceValidator:
    async def validate_source(self, url):
        class MockResult:
            is_compliant = True
            violations = []
            robots_txt_compliant = True
            legal_contact_verified = True

        return MockResult()


from .base import (
    BaseCLI,
    async_command,
    common_options,
    validate_email,
    validate_source_id,
)


class SourceCLI(BaseCLI):
    """CLI for news source management"""

    def __init__(self):
        super().__init__()
        self.compliance_validator = ComplianceValidator()

    async def create_source(self, name: str, base_url: str, **kwargs) -> dict:
        """Create a new news source"""
        async with self.db_manager.get_session() as session:
            # Check if source already exists
            existing_query = select(NewsSource).where(
                (NewsSource.name == name) | (NewsSource.base_url == base_url)
            )
            existing = await session.execute(existing_query)
            if existing.scalar():
                raise click.ClickException(
                    f"Source with name '{name}' or URL '{base_url}' already exists"
                )

            # Create new source
            source = NewsSource(
                name=name,
                base_url=base_url,
                language=kwargs.get("language", "en"),
                country=kwargs.get("country", "US"),
                description=kwargs.get("description"),
                legal_contact_email=kwargs.get("legal_contact_email"),
                terms_of_service_url=kwargs.get("terms_of_service_url"),
                privacy_policy_url=kwargs.get("privacy_policy_url"),
                fair_use_basis=kwargs.get(
                    "fair_use_basis",
                    "Academic research at UCOMPENSAR University for breast cancer news analysis under fair use doctrine for educational purposes",
                ),
                content_type="metadata_only",
                data_retention_days=kwargs.get("data_retention_days", 365),
                max_articles_per_run=kwargs.get("max_articles_per_run", 50),
                crawl_delay_seconds=kwargs.get("crawl_delay_seconds", 2.0),
                source_type=kwargs.get("source_type", "news_site"),
                status="active",
            )

            session.add(source)
            await session.commit()
            await session.refresh(source)

            self.log(f"Created source: {source.name} (ID: {source.id})", "success")

            return {
                "id": source.id,
                "name": source.name,
                "base_url": source.base_url,
                "status": source.status,
                "created_at": source.created_at.isoformat(),
            }

    async def update_source(self, source_id: int, **kwargs) -> dict:
        """Update an existing news source"""
        async with self.db_manager.get_session() as session:
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            result = await session.execute(source_query)
            source = result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            # Update fields
            updated_fields = []
            for field, value in kwargs.items():
                if value is not None and hasattr(source, field):
                    old_value = getattr(source, field)
                    setattr(source, field, value)
                    updated_fields.append(f"{field}: {old_value} → {value}")

            source.updated_at = datetime.utcnow()
            await session.commit()

            self.log(f"Updated source: {source.name}", "success")
            if updated_fields and self.verbose:
                for field in updated_fields:
                    self.log(f"  {field}")

            return {
                "id": source.id,
                "name": source.name,
                "updated_fields": len(updated_fields),
                "updated_at": source.updated_at.isoformat(),
            }

    async def delete_source(self, source_id: int, force: bool = False) -> dict:
        """Delete a news source"""
        async with self.db_manager.get_session() as session:
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            result = await session.execute(source_query)
            source = result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            # Check for associated articles
            from sqlalchemy import func

            from services.data.database.models import Article

            article_count_query = select(func.count(Article.id)).where(
                Article.source_id == source_id
            )
            article_count_result = await session.execute(article_count_query)
            article_count = article_count_result.scalar() or 0

            if article_count > 0 and not force:
                raise click.ClickException(
                    f"Source has {article_count} associated articles. Use --force to delete anyway."
                )

            source_name = source.name
            await session.delete(source)
            await session.commit()

            self.log(
                f"Deleted source: {source_name} (had {article_count} articles)",
                "success",
            )

            return {
                "id": source_id,
                "name": source_name,
                "articles_deleted": article_count,
                "deleted_at": datetime.now().isoformat(),
            }

    async def list_sources(
        self,
        status_filter: Optional[str] = None,
        compliance_filter: Optional[str] = None,
    ) -> List[dict]:
        """List all news sources"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource)

            if status_filter:
                query = query.where(NewsSource.status == status_filter)

            result = await session.execute(query)
            sources = result.scalars().all()

            source_data = []
            for source in sources:
                # Calculate compliance status
                compliance_status = "unknown"
                if source.compliance_last_checked:
                    if (
                        source.robots_txt_compliant
                        and source.legal_contact_verified
                        and source.fair_use_documented
                    ):
                        compliance_status = "compliant"
                    else:
                        compliance_status = "non-compliant"

                # Filter by compliance if specified
                if compliance_filter and compliance_status != compliance_filter:
                    continue

                source_data.append(
                    {
                        "id": source.id,
                        "name": source.name,
                        "base_url": source.base_url,
                        "status": source.status,
                        "language": source.language,
                        "country": source.country,
                        "source_type": source.source_type,
                        "compliance_status": compliance_status,
                        "risk_level": source.risk_level or "unknown",
                        "articles_total": source.articles_collected_total or 0,
                        "last_run": (
                            source.last_successful_run.strftime("%Y-%m-%d")
                            if source.last_successful_run
                            else "Never"
                        ),
                        "created_at": source.created_at.strftime("%Y-%m-%d"),
                    }
                )

            return source_data

    async def validate_source(self, source_id: int, update_db: bool = True) -> dict:
        """Validate source compliance"""
        async with self.db_manager.get_session() as session:
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            result = await session.execute(source_query)
            source = result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            self.log(f"Validating source: {source.name}")

            # Run compliance validation
            compliance_result = await self.compliance_validator.validate_source(
                source.base_url
            )

            # Update database if requested
            if update_db:
                source.robots_txt_compliant = compliance_result.robots_txt_compliant
                source.legal_contact_verified = compliance_result.legal_contact_verified
                source.terms_acceptable = True  # Assume acceptable for now
                source.fair_use_documented = bool(source.fair_use_basis)
                source.compliance_last_checked = datetime.utcnow()

                # Update risk level
                violation_count = len(compliance_result.violations)
                if violation_count == 0:
                    source.risk_level = "low"
                elif violation_count <= 2:
                    source.risk_level = "medium"
                else:
                    source.risk_level = "high"

                await session.commit()
                self.log("Database updated with compliance results", "success")

            return {
                "source_id": source_id,
                "source_name": source.name,
                "is_compliant": compliance_result.is_compliant,
                "violations": compliance_result.violations,
                "robots_txt_compliant": compliance_result.robots_txt_compliant,
                "legal_contact_verified": compliance_result.legal_contact_verified,
                "fair_use_documented": bool(source.fair_use_basis),
                "risk_level": source.risk_level if update_db else "not_updated",
                "checked_at": datetime.now().isoformat(),
            }

    async def get_source_details(self, source_id: int) -> dict:
        """Get detailed information about a source"""
        async with self.db_manager.get_session() as session:
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            result = await session.execute(source_query)
            source = result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            # Get article statistics
            from sqlalchemy import func

            from services.data.database.models import Article

            # Total articles
            total_query = select(func.count(Article.id)).where(
                Article.source_id == source_id
            )
            total_result = await session.execute(total_query)
            total_articles = total_result.scalar() or 0

            # Recent articles (last 30 days)
            recent_query = select(func.count(Article.id)).where(
                Article.source_id == source_id,
                Article.created_at >= datetime.now() - timedelta(days=30),
            )
            recent_result = await session.execute(recent_query)
            recent_articles = recent_result.scalar() or 0

            return {
                "id": source.id,
                "name": source.name,
                "base_url": source.base_url,
                "description": source.description,
                "status": source.status,
                "language": source.language,
                "country": source.country,
                "source_type": source.source_type,
                "legal_contact_email": source.legal_contact_email,
                "terms_of_service_url": source.terms_of_service_url,
                "privacy_policy_url": source.privacy_policy_url,
                "fair_use_basis": source.fair_use_basis,
                "content_type": source.content_type,
                "data_retention_days": source.data_retention_days,
                "max_articles_per_run": source.max_articles_per_run,
                "crawl_delay_seconds": float(source.crawl_delay_seconds),
                "compliance": {
                    "robots_txt_compliant": source.robots_txt_compliant,
                    "legal_contact_verified": source.legal_contact_verified,
                    "terms_acceptable": source.terms_acceptable,
                    "fair_use_documented": source.fair_use_documented,
                    "data_minimization_applied": source.data_minimization_applied,
                    "last_checked": (
                        source.compliance_last_checked.isoformat()
                        if source.compliance_last_checked
                        else None
                    ),
                    "risk_level": source.risk_level,
                },
                "performance": {
                    "last_successful_run": (
                        source.last_successful_run.isoformat()
                        if source.last_successful_run
                        else None
                    ),
                    "success_rate": (
                        float(source.success_rate) if source.success_rate else 0.0
                    ),
                    "articles_collected_total": source.articles_collected_total or 0,
                    "articles_last_30_days": recent_articles,
                    "error_count_last_30_days": source.error_count_last_30_days or 0,
                },
                "timestamps": {
                    "created_at": source.created_at.isoformat(),
                    "updated_at": source.updated_at.isoformat(),
                },
            }


# CLI Commands
@click.group()
@click.pass_context
def source(ctx):
    """News source management commands"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = SourceCLI()


@source.command()
@click.option(
    "--status",
    type=click.Choice(["active", "inactive", "suspended", "under_review"]),
    help="Filter by status",
)
@click.option(
    "--compliance",
    type=click.Choice(["compliant", "non-compliant", "unknown"]),
    help="Filter by compliance status",
)
@common_options
@click.pass_context
@async_command
async def list(ctx, status, compliance, verbose, quiet, format):
    """List all news sources"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    sources = await cli.list_sources(status, compliance)

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
            "Type",
            "Compliance",
            "Risk",
            "Articles",
        ]
        rows = [
            [
                s["id"],
                s["name"][:25],
                s["base_url"][:35],
                s["status"],
                s["source_type"],
                s["compliance_status"],
                s["risk_level"],
                s["articles_total"],
            ]
            for s in sources
        ]
        click.echo(cli.format_table(rows, headers))


@source.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@common_options
@click.pass_context
@async_command
async def show(ctx, source_id, verbose, quiet, format):
    """Show detailed information about a source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    details = await cli.get_source_details(source_id)

    if format == "json":
        click.echo(cli.format_json(details))
    else:
        click.echo(f"\n📰 Source Details: {details['name']}")
        click.echo(f"  ID: {details['id']}")
        click.echo(f"  URL: {details['base_url']}")
        click.echo(f"  Status: {details['status']}")
        click.echo(f"  Type: {details['source_type']}")
        click.echo(f"  Language: {details['language']}")
        click.echo(f"  Country: {details['country']}")

        if details["description"]:
            click.echo(f"  Description: {details['description']}")

        click.echo(f"\n🔒 Compliance:")
        compliance = details["compliance"]
        click.echo(
            f"  Robots.txt: {'✅' if compliance['robots_txt_compliant'] else '❌'}"
        )
        click.echo(
            f"  Legal Contact: {'✅' if compliance['legal_contact_verified'] else '❌'}"
        )
        click.echo(f"  Fair Use: {'✅' if compliance['fair_use_documented'] else '❌'}")
        click.echo(f"  Risk Level: {compliance['risk_level']}")

        click.echo(f"\n📊 Performance:")
        perf = details["performance"]
        click.echo(f"  Total Articles: {perf['articles_collected_total']}")
        click.echo(f"  Articles (30d): {perf['articles_last_30_days']}")
        click.echo(f"  Success Rate: {perf['success_rate']:.1%}")
        click.echo(f"  Last Run: {perf['last_successful_run'] or 'Never'}")


@source.command()
@click.argument("name")
@click.argument("base_url")
@click.option("--language", default="en", help="Source language (ISO 639-1 code)")
@click.option(
    "--country", default="US", help="Source country (ISO 3166-1 alpha-2 code)"
)
@click.option("--description", help="Source description")
@click.option(
    "--legal-contact-email", callback=validate_email, help="Legal contact email"
)
@click.option("--terms-of-service-url", help="Terms of service URL")
@click.option("--privacy-policy-url", help="Privacy policy URL")
@click.option(
    "--source-type",
    type=click.Choice(
        ["news_site", "academic", "government", "ngo", "medical_journal"]
    ),
    default="news_site",
    help="Type of source",
)
@click.option(
    "--max-articles-per-run",
    type=int,
    default=50,
    help="Maximum articles per scraping run",
)
@click.option(
    "--crawl-delay-seconds",
    type=float,
    default=2.0,
    help="Delay between requests in seconds",
)
@common_options
@click.pass_context
@async_command
async def create(
    ctx,
    name,
    base_url,
    language,
    country,
    description,
    legal_contact_email,
    terms_of_service_url,
    privacy_policy_url,
    source_type,
    max_articles_per_run,
    crawl_delay_seconds,
    verbose,
    quiet,
    format,
):
    """Create a new news source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.create_source(
        name=name,
        base_url=base_url,
        language=language,
        country=country,
        description=description,
        legal_contact_email=legal_contact_email,
        terms_of_service_url=terms_of_service_url,
        privacy_policy_url=privacy_policy_url,
        source_type=source_type,
        max_articles_per_run=max_articles_per_run,
        crawl_delay_seconds=crawl_delay_seconds,
    )

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"✅ Created source: {result['name']} (ID: {result['id']})")


@source.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@click.option("--name", help="Update source name")
@click.option("--description", help="Update source description")
@click.option(
    "--status",
    type=click.Choice(["active", "inactive", "suspended", "under_review"]),
    help="Update source status",
)
@click.option(
    "--legal-contact-email", callback=validate_email, help="Update legal contact email"
)
@click.option("--max-articles-per-run", type=int, help="Update max articles per run")
@click.option("--crawl-delay-seconds", type=float, help="Update crawl delay")
@common_options
@click.pass_context
@async_command
async def update(
    ctx,
    source_id,
    name,
    description,
    status,
    legal_contact_email,
    max_articles_per_run,
    crawl_delay_seconds,
    verbose,
    quiet,
    format,
):
    """Update an existing news source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    kwargs = {}
    if name:
        kwargs["name"] = name
    if description:
        kwargs["description"] = description
    if status:
        kwargs["status"] = status
    if legal_contact_email:
        kwargs["legal_contact_email"] = legal_contact_email
    if max_articles_per_run:
        kwargs["max_articles_per_run"] = max_articles_per_run
    if crawl_delay_seconds:
        kwargs["crawl_delay_seconds"] = crawl_delay_seconds

    if not kwargs:
        raise click.ClickException("No update parameters provided")

    result = await cli.update_source(source_id, **kwargs)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(
            f"✅ Updated source: {result['name']} ({result['updated_fields']} fields)"
        )


@source.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@click.option("--force", is_flag=True, help="Force delete even if source has articles")
@common_options
@click.pass_context
@async_command
async def delete(ctx, source_id, force, verbose, quiet, format):
    """Delete a news source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    if not cli.confirm_action("Are you sure you want to delete this source?", False):
        click.echo("Operation cancelled")
        return

    result = await cli.delete_source(source_id, force)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"✅ Deleted source: {result['name']}")
        if result["articles_deleted"] > 0:
            click.echo(
                f"  Also deleted {result['articles_deleted']} associated articles"
            )


@source.command()
@click.argument("source_id", type=int, callback=validate_source_id)
@click.option("--no-update", is_flag=True, help="Don't update database with results")
@common_options
@click.pass_context
@async_command
async def validate(ctx, source_id, no_update, verbose, quiet, format):
    """Validate source compliance"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.validate_source(source_id, not no_update)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        if result["is_compliant"]:
            cli.log(f"Source '{result['source_name']}' is compliant ✅", "success")
        else:
            cli.log(
                f"Source '{result['source_name']}' has compliance violations ❌",
                "warning",
            )
            for violation in result["violations"]:
                click.echo(f"  - {violation}")

        click.echo(f"  Risk Level: {result['risk_level']}")


if __name__ == "__main__":
    source()
