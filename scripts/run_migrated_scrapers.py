#!/usr/bin/env python3
"""
Script para ejecutar scrapers migrados a PostgreSQL
Usage: python scripts/run_migrated_scrapers.py [scraper_name]
"""

import asyncio
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

load_dotenv()

from services.data.database.connection import close_database, init_database

# Import migrated scrapers
from services.scraper.src.extractors.www_breastcancer_org_postgres import (
    scrape_breastcancer_org_to_postgres,
)
from services.scraper.src.extractors.www_curetoday_com_postgres import (
    scrape_curetoday_to_postgres,
)
from services.scraper.src.extractors.www_news_medical_net_postgres import (
    scrape_news_medical_to_postgres,
)
from services.scraper.src.extractors.www_webmd_com_postgres import (
    scrape_webmd_to_postgres,
)

AVAILABLE_SCRAPERS = {
    "breastcancer.org": scrape_breastcancer_org_to_postgres,
    "webmd.com": scrape_webmd_to_postgres,
    "curetoday.com": scrape_curetoday_to_postgres,
    "news-medical.net": scrape_news_medical_to_postgres,
    # Add more scrapers as they are migrated
}


async def run_scraper(scraper_name: str):
    """Run a specific migrated scraper"""
    if scraper_name not in AVAILABLE_SCRAPERS:
        print(f"❌ Scraper '{scraper_name}' not found.")
        print(f"Available scrapers: {', '.join(AVAILABLE_SCRAPERS.keys())}")
        return

    print(f"🚀 Running migrated scraper: {scraper_name}")
    print(f"⏰ Started at: {datetime.now()}")

    try:
        await init_database()
        scraper_func = AVAILABLE_SCRAPERS[scraper_name]
        article_ids = await scraper_func()

        print(f"\n✅ Scraper completed successfully!")
        print(f"📊 Articles inserted: {len(article_ids)}")
        print(
            f"🆔 Article IDs: {article_ids[:10]}{'...' if len(article_ids) > 10 else ''}"
        )

    except Exception as e:
        print(f"❌ Error running scraper: {e}")
        raise
    finally:
        await close_database()


async def run_all_scrapers():
    """Run all available migrated scrapers"""
    print(f"🚀 Running ALL migrated scrapers ({len(AVAILABLE_SCRAPERS)})")

    total_articles = 0
    for scraper_name in AVAILABLE_SCRAPERS.keys():
        print(f"\n{'='*60}")
        print(f"Running: {scraper_name}")
        print(f"{'='*60}")

        try:
            await init_database()
            scraper_func = AVAILABLE_SCRAPERS[scraper_name]
            article_ids = await scraper_func()
            total_articles += len(article_ids)
            print(f"✅ {scraper_name}: {len(article_ids)} articles")
        except Exception as e:
            print(f"❌ {scraper_name} failed: {e}")
        finally:
            await close_database()

    print(f"\n🎯 SUMMARY:")
    print(f"   📊 Total articles inserted: {total_articles}")
    print(f"   ✅ Scrapers completed: {len(AVAILABLE_SCRAPERS)}")


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_migrated_scrapers.py [scraper_name|all]")
        print(f"Available scrapers: {', '.join(AVAILABLE_SCRAPERS.keys())}")
        print("Use 'all' to run all scrapers")
        sys.exit(1)

    target = sys.argv[1].lower()

    if target == "all":
        asyncio.run(run_all_scrapers())
    else:
        asyncio.run(run_scraper(target))


if __name__ == "__main__":
    main()
