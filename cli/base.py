"""
Base CLI framework for PreventIA News Analytics
Provides common functionality for all CLI tools
"""

import asyncio
import sys
from datetime import datetime
from typing import Any, Dict, Optional

import click

from services.api.auth.role_manager import initialize_role_manager
from services.data.database.connection import db_manager


class BaseCLI:
    """Base class for all CLI tools with common functionality"""

    def __init__(self):
        self.db_manager = db_manager  # Use global instance
        self.verbose = False
        self.quiet = False

    async def initialize(self):
        """Initialize database connection and authentication system"""
        try:
            await self.db_manager.initialize()

            # Initialize role manager
            initialize_role_manager(self.db_manager)

            if not self.quiet:
                click.echo("✅ Database connection established")
                click.echo("🔐 Authentication system initialized")
        except Exception as e:
            click.echo(f"❌ Failed to initialize: {e}", err=True)
            sys.exit(1)

    async def cleanup(self):
        """Clean up database connections"""
        if self.db_manager:
            await self.db_manager.close()
            if not self.quiet:
                click.echo("🔴 Database connection closed")

    def log(self, message: str, level: str = "info"):
        """Log messages with appropriate formatting"""
        if self.quiet and level != "error":
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if level == "error":
            click.echo(f"❌ [{timestamp}] ERROR: {message}", err=True)
        elif level == "warning":
            click.echo(f"⚠️  [{timestamp}] WARNING: {message}")
        elif level == "success":
            click.echo(f"✅ [{timestamp}] SUCCESS: {message}")
        elif level == "info" and self.verbose:
            click.echo(f"ℹ️  [{timestamp}] INFO: {message}")
        elif level == "debug" and self.verbose:
            click.echo(f"🔍 [{timestamp}] DEBUG: {message}")

    def format_table(self, data: list, headers: list) -> str:
        """Format data as a simple table"""
        if not data:
            return "No data to display"

        # Calculate column widths
        widths = [len(header) for header in headers]
        for row in data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Create format string
        format_str = " | ".join(f"{{:<{width}}}" for width in widths)

        # Build table
        lines = []
        lines.append(format_str.format(*headers))
        lines.append("-" * (sum(widths) + 3 * (len(headers) - 1)))

        for row in data:
            lines.append(format_str.format(*[str(cell) for cell in row]))

        return "\n".join(lines)

    def format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON"""
        import json

        return json.dumps(data, indent=2, default=str)

    def confirm_action(self, message: str, default: bool = False) -> bool:
        """Ask for user confirmation"""
        if self.quiet:
            return default

        suffix = " [Y/n]" if default else " [y/N]"
        return click.confirm(message + suffix, default=default)

    def run_async(self, coro):
        """Run an async coroutine from sync context"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)


def async_command(f):
    """Decorator to handle async CLI commands"""

    def wrapper(*args, **kwargs):
        cli = args[0] if args and isinstance(args[0], BaseCLI) else None

        async def async_wrapper():
            try:
                if cli:
                    await cli.initialize()
                result = await f(*args, **kwargs)
                if cli:
                    await cli.cleanup()
                return result
            except Exception as e:
                if cli:
                    cli.log(f"Command failed: {e}", "error")
                    await cli.cleanup()
                raise

        return asyncio.run(async_wrapper())

    return wrapper


def common_options(f):
    """Common CLI options decorator"""
    f = click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")(f)
    f = click.option(
        "--quiet", "-q", is_flag=True, help="Suppress output except errors"
    )(f)
    f = click.option(
        "--format",
        type=click.Choice(["table", "json"]),
        default="table",
        help="Output format",
    )(f)
    return f


def validate_source_id(ctx, param, value):
    """Validate source ID parameter"""
    if value is not None and value <= 0:
        raise click.BadParameter("Source ID must be a positive integer")
    return value


def validate_email(ctx, param, value):
    """Validate email parameter"""
    if value is not None:
        import re

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, value):
            raise click.BadParameter("Invalid email format")
    return value
