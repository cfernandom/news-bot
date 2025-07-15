#!/usr/bin/env python3
"""
Legal Compliance Migration Script for PreventIA News Analytics
Applies database schema changes and compliance checks to existing data.

Usage:
    python scripts/apply_legal_compliance.py [--dry-run] [--backup]

Created: 2025-06-29
Purpose: Implement legal compliance measures for existing data
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()
from datetime import datetime, timedelta
from pathlib import Path

from services.data.database.connection import DatabaseManager
from services.scraper.src.compliance import check_robots_compliance

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LegalComplianceMigrator:
    """Handles migration of existing data to legal compliance standards."""

    def __init__(self, db_manager: DatabaseManager, dry_run: bool = False):
        self.db_manager = db_manager
        self.dry_run = dry_run
        self.stats = {
            "articles_processed": 0,
            "articles_marked_for_review": 0,
            "sources_updated": 0,
            "robots_checks_performed": 0,
            "retention_dates_set": 0,
        }

    async def apply_database_migration(self):
        """Apply the 002_legal_compliance.sql migration."""
        logger.info("Applying legal compliance database migration...")

        project_root = Path(__file__).parent.parent
        migration_file = (
            project_root / "services/data/database/migrations/002_legal_compliance.sql"
        )

        if not migration_file.exists():
            logger.error(f"Migration file not found: {migration_file}")
            return False

        try:
            with open(migration_file, "r") as f:
                migration_sql = f.read()

            if self.dry_run:
                logger.info("DRY RUN: Would apply database migration")
                logger.info(
                    f"Migration SQL preview (first 200 chars): {migration_sql[:200]}..."
                )
                return True

            # Apply migration using asyncpg connection
            async with self.db_manager.get_connection() as conn:
                await conn.execute(migration_sql)
            logger.info("✅ Database migration applied successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error applying database migration: {e}")
            return False

    async def update_existing_articles(self):
        """Update existing articles with compliance metadata."""
        logger.info("Updating existing articles with compliance data...")

        try:
            # Get all existing articles that need compliance review
            articles_query = """
                SELECT id, url, scraped_at, source_id
                FROM articles
                WHERE legal_review_status IN ('pending', 'needs_review') OR legal_review_status IS NULL
                ORDER BY id
            """

            articles = await self.db_manager.execute_sql(articles_query)
            logger.info(f"Found {len(articles)} articles to process")

            for article in articles:
                await self._process_article_compliance(article)
                self.stats["articles_processed"] += 1

                # Progress logging
                if self.stats["articles_processed"] % 10 == 0:
                    logger.info(
                        f"Processed {self.stats['articles_processed']}/{len(articles)} articles"
                    )

            logger.info(f"✅ Processed {self.stats['articles_processed']} articles")

        except Exception as e:
            logger.error(f"❌ Error updating articles: {e}")

    async def _process_article_compliance(self, article):
        """Process compliance for a single article."""
        article_id = article["id"]
        url = article["url"]
        scraped_at = article["scraped_at"]

        try:
            # Check robots.txt compliance (simplified for existing data)
            robots_compliant = await self._check_robots_compliance(url)

            # Set data retention expiry (1 year from scraping)
            retention_expires = scraped_at + timedelta(days=365)

            # Determine content type (existing articles have full content)
            content_type = "full"  # Existing data

            # Set initial compliance status
            legal_review_status = "needs_review"
            copyright_status = "unknown"

            if self.dry_run:
                logger.debug(
                    f"DRY RUN: Would update article {article_id} with compliance data"
                )
                return

            # Update article with compliance data
            update_query = """
                UPDATE articles
                SET
                    robots_txt_compliant = $1,
                    copyright_status = $2,
                    content_type = $3,
                    legal_review_status = $4,
                    data_retention_expires_at = $5,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = $6
            """

            async with self.db_manager.get_connection() as conn:
                await conn.execute(
                    update_query,
                    robots_compliant,
                    copyright_status,
                    content_type,
                    legal_review_status,
                    retention_expires,
                    article_id,
                )

            self.stats["articles_marked_for_review"] += 1
            self.stats["robots_checks_performed"] += 1
            self.stats["retention_dates_set"] += 1

        except Exception as e:
            logger.error(f"Error processing article {article_id}: {e}")

    async def _check_robots_compliance(self, url: str) -> bool:
        """Check robots.txt compliance for a URL."""
        try:
            # For existing data, we assume compliance unless explicitly blocked
            # In production, you might want to do actual robots.txt checks
            is_compliant = await check_robots_compliance(url)
            return is_compliant
        except Exception as e:
            logger.warning(f"Could not check robots.txt for {url}: {e}")
            return None  # Unknown compliance status

    async def update_news_sources(self):
        """Update news sources with compliance metadata."""
        logger.info("Updating news sources with compliance data...")

        try:
            # Get all news sources
            sources_query = "SELECT id, base_url, name FROM news_sources"
            sources = await self.db_manager.execute_sql(sources_query)

            for source in sources:
                await self._process_source_compliance(source)
                self.stats["sources_updated"] += 1

            logger.info(f"✅ Updated {self.stats['sources_updated']} news sources")

        except Exception as e:
            logger.error(f"❌ Error updating news sources: {e}")

    async def _process_source_compliance(self, source):
        """Process compliance for a single news source."""
        source_id = source["id"]
        base_url = source["base_url"]

        try:
            # Generate robots.txt URL
            robots_url = f"{base_url.rstrip('/')}/robots.txt"

            # Set default crawl delay
            crawl_delay = 2  # seconds

            if self.dry_run:
                logger.debug(
                    f"DRY RUN: Would update source {source_id} with compliance data"
                )
                return

            # Update source with compliance data
            update_query = """
                UPDATE news_sources
                SET
                    robots_txt_url = $1,
                    crawl_delay_seconds = $2,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = $3
            """

            async with self.db_manager.get_connection() as conn:
                await conn.execute(update_query, robots_url, crawl_delay, source_id)

        except Exception as e:
            logger.error(f"Error processing source {source_id}: {e}")

    async def create_compliance_audit_entry(self):
        """Create audit log entry for this migration."""
        if self.dry_run:
            logger.info("DRY RUN: Would create compliance audit entry")
            return

        try:
            audit_query = """
                INSERT INTO compliance_audit_log
                (table_name, record_id, action, status, details, performed_by)
                VALUES ($1, $2, $3, $4, $5, $6)
            """

            import json

            details = json.dumps(
                {
                    "migration_type": "legal_compliance_update",
                    "articles_processed": self.stats["articles_processed"],
                    "sources_updated": self.stats["sources_updated"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

            async with self.db_manager.get_connection() as conn:
                await conn.execute(
                    audit_query,
                    "system",
                    0,
                    "compliance_migration",
                    "completed",
                    details,
                    "migration_script",
                )

            logger.info("✅ Compliance audit entry created")

        except Exception as e:
            logger.error(f"❌ Error creating audit entry: {e}")

    def print_summary(self):
        """Print migration summary."""
        print("\n" + "=" * 60)
        print("LEGAL COMPLIANCE MIGRATION SUMMARY")
        print("=" * 60)
        print(f"Articles processed: {self.stats['articles_processed']}")
        print(f"Articles marked for review: {self.stats['articles_marked_for_review']}")
        print(f"Sources updated: {self.stats['sources_updated']}")
        print(f"Robots.txt checks performed: {self.stats['robots_checks_performed']}")
        print(f"Retention dates set: {self.stats['retention_dates_set']}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE MIGRATION'}")
        print("=" * 60)

        if self.dry_run:
            print("\n⚠️  This was a DRY RUN. No changes were made to the database.")
            print("   Run without --dry-run to apply changes.")
        else:
            print("\n✅ Migration completed successfully!")
            print("   Next steps:")
            print("   1. Review articles marked as 'needs_review'")
            print("   2. Update privacy policy and terms of service")
            print("   3. Implement robots.txt checking in scrapers")
            print("   4. Set up regular compliance monitoring")


async def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(
        description="Apply legal compliance measures to PreventIA database"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create database backup before migration (recommended)",
    )

    args = parser.parse_args()

    if args.backup and not args.dry_run:
        logger.warning("⚠️  Backup option not implemented yet. Proceeding anyway.")
        logger.warning("   Consider manually backing up your database first.")

    # Initialize database manager
    db_manager = DatabaseManager()

    try:
        # Initialize database connection
        await db_manager.initialize()
        logger.info("✅ Database connection established")

        # Create migrator
        migrator = LegalComplianceMigrator(db_manager, dry_run=args.dry_run)

        # Run migration steps
        logger.info("Starting legal compliance migration...")

        # 1. Apply database schema changes
        success = await migrator.apply_database_migration()
        if not success:
            logger.error("❌ Database migration failed. Stopping.")
            return 1

        # 2. Update existing articles
        await migrator.update_existing_articles()

        # 3. Update news sources
        await migrator.update_news_sources()

        # 4. Create audit entry
        await migrator.create_compliance_audit_entry()

        # 5. Print summary
        migrator.print_summary()

        return 0

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return 1

    finally:
        await db_manager.close()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
