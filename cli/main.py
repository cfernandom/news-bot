#!/usr/bin/env python3
"""
PreventIA News Analytics CLI
Command-line interface for system management and automation
"""

import os
import sys
from pathlib import Path

import click

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.compliance_cli import compliance
from cli.scraper_cli import scraper
from cli.source_cli import source
from cli.user_cli import user


@click.group()
@click.version_option(version="1.0.0", prog_name="PreventIA CLI")
@click.pass_context
def cli(ctx):
    """
    PreventIA News Analytics CLI

    Command-line interface for managing news sources, scrapers, users, and compliance.

    \b
    Available Commands:
      scraper     - Scraper management and automation
      source      - News source administration
      user        - User and role management
      compliance  - Legal compliance monitoring

    \b
    Examples:
      preventia-cli scraper list
      preventia-cli source create "Medical News" https://example.com
      preventia-cli user create john john@example.com "John Doe"
      preventia-cli compliance dashboard

    \b
    Environment Variables:
      DATABASE_URL        - PostgreSQL connection string
      JWT_SECRET_KEY      - JWT token secret key
      API_HOST           - API server host (default: 0.0.0.0)
      API_PORT           - API server port (default: 8000)

    For detailed help on any command, use: preventia-cli COMMAND --help
    """
    ctx.ensure_object(dict)

    # Set environment variables if not set
    if not os.getenv("DATABASE_URL"):
        os.environ["DATABASE_URL"] = (
            "postgresql://preventia:preventia@localhost:5433/preventia_news"
        )

    if not os.getenv("JWT_SECRET_KEY"):
        click.echo(
            "⚠️  Warning: JWT_SECRET_KEY not set. Using default (not secure for production)",
            err=True,
        )
        os.environ["JWT_SECRET_KEY"] = "preventia-dev-key-change-in-production"


# Add subcommands
cli.add_command(scraper)
cli.add_command(source)
cli.add_command(user)
cli.add_command(compliance)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def status(verbose):
    """Show system status and health check"""
    import asyncio

    from services.data.database.connection import DatabaseManager

    async def check_status():
        click.echo("🔍 Checking system status...")

        try:
            # Database connection
            db_manager = DatabaseManager()
            await db_manager.initialize()

            is_healthy = await db_manager.health_check()
            if is_healthy:
                click.echo("✅ Database: Connected")
            else:
                click.echo("❌ Database: Connection failed")
                return

            # Check tables
            tables_query = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
            """
            tables_result = await db_manager.execute_sql(tables_query)
            table_count = len(tables_result)
            click.echo(f"📊 Database Tables: {table_count}")

            if verbose:
                for table in tables_result:
                    click.echo(f"   - {table['table_name']}")

            # Check articles
            articles_query = "SELECT COUNT(*) as count FROM articles"
            articles_result = await db_manager.execute_sql(articles_query)
            article_count = articles_result[0]["count"] if articles_result else 0
            click.echo(f"📰 Articles: {article_count}")

            # Check sources
            sources_query = (
                "SELECT COUNT(*) as count FROM news_sources WHERE is_active = true"
            )
            sources_result = await db_manager.execute_sql(sources_query)
            source_count = sources_result[0]["count"] if sources_result else 0
            click.echo(f"🌐 Active Sources: {source_count}")

            # Check users
            users_query = "SELECT COUNT(*) as count FROM users WHERE is_active = true"
            users_result = await db_manager.execute_sql(users_query)
            user_count = users_result[0]["count"] if users_result else 0
            click.echo(f"👤 Active Users: {user_count}")

            click.echo("✅ System status: Healthy")

            await db_manager.close()

        except Exception as e:
            click.echo(f"❌ System status check failed: {e}", err=True)
            sys.exit(1)

    asyncio.run(check_status())


@cli.command()
@click.option("--host", default="0.0.0.0", help="API server host")
@click.option("--port", type=int, default=8000, help="API server port")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
def serve(host, port, reload):
    """Start the FastAPI server"""
    import uvicorn

    click.echo(f"🚀 Starting PreventIA API server on {host}:{port}")
    if reload:
        click.echo("🔄 Auto-reload enabled for development")

    try:
        uvicorn.run(
            "services.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
        )
    except KeyboardInterrupt:
        click.echo("\n🔴 Server stopped")


@cli.command()
@click.option("--backup-file", type=click.Path(), help="Backup file path")
@click.option(
    "--tables", multiple=True, help="Specific tables to backup (default: all)"
)
def backup(backup_file, tables):
    """Backup database to file"""
    import asyncio
    import json
    from datetime import datetime

    from services.data.database.connection import DatabaseManager

    if not backup_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"preventia_backup_{timestamp}.json"

    async def create_backup():
        click.echo(f"📦 Creating database backup: {backup_file}")

        try:
            db_manager = DatabaseManager()
            await db_manager.initialize()

            backup_data = {"timestamp": datetime.now().isoformat(), "tables": {}}

            # Default tables to backup
            default_tables = [
                "news_sources",
                "articles",
                "users",
                "user_roles",
                "user_role_assignments",
                "compliance_audit_log",
                "legal_notices",
            ]

            tables_to_backup = list(tables) if tables else default_tables

            for table_name in tables_to_backup:
                try:
                    click.echo(f"  Backing up table: {table_name}")
                    result = await db_manager.execute_sql(f"SELECT * FROM {table_name}")
                    backup_data["tables"][table_name] = result
                    click.echo(f"    ✅ {len(result)} records")
                except Exception as e:
                    click.echo(f"    ❌ Error: {e}")

            # Write backup file
            with open(backup_file, "w") as f:
                json.dump(backup_data, f, indent=2, default=str)

            click.echo(f"✅ Backup completed: {backup_file}")

            await db_manager.close()

        except Exception as e:
            click.echo(f"❌ Backup failed: {e}", err=True)
            sys.exit(1)

    asyncio.run(create_backup())


@cli.command()
def version():
    """Show version information"""
    click.echo("PreventIA News Analytics CLI v1.0.0")
    click.echo("Copyright (c) 2025 UCOMPENSAR University")
    click.echo("Licensed for academic research use")


@cli.command()
def docs():
    """Show documentation links"""
    click.echo("📚 PreventIA Documentation:")
    click.echo("")
    click.echo("  API Documentation:")
    click.echo("    http://localhost:8000/docs (OpenAPI/Swagger)")
    click.echo("    http://localhost:8000/redoc (ReDoc)")
    click.echo("")
    click.echo("  Project Documentation:")
    click.echo("    docs/README.md - Documentation hub")
    click.echo("    docs/api/ - API documentation")
    click.echo("    docs/development/ - Development guides")
    click.echo("    docs/operations/ - Operations and deployment")
    click.echo("")
    click.echo("  Quick Start:")
    click.echo("    preventia-cli status        - Check system health")
    click.echo("    preventia-cli scraper list  - List all scrapers")
    click.echo("    preventia-cli source list   - List news sources")
    click.echo("    preventia-cli user list     - List users")


from .compliance_cli import compliance

# Add sub-command groups
from .scraper_cli import scraper
from .source_cli import source
from .user_cli import user

cli.add_command(scraper)
cli.add_command(source)
cli.add_command(user)
cli.add_command(compliance)


if __name__ == "__main__":
    cli()
