"""
Migrated scraper for breastcancer.org - PostgreSQL Storage
Phase 1: Direct database storage with analytics-ready structure
"""

import asyncio
import hashlib
import os
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()
from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Add project root to path for imports
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from services.data.database.connection import db_manager


def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_breastcancer_source_id() -> Optional[int]:
    """Get the source_id for breastcancer.org from news_sources table"""
    query = (
        "SELECT id FROM news_sources WHERE base_url LIKE '%breastcancer.org%' LIMIT 1"
    )
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


async def scrape_breastcancer_org_to_postgres() -> List[int]:
    """
    Migrated scraper that stores articles directly in PostgreSQL
    Returns: List of inserted article IDs
    """
    URL = "https://www.breastcancer.org/research-news"
    BASE_URL = "https://www.breastcancer.org"

    print(f"🔍 Starting scrape of {URL}")

    # Get source_id from database
    source_id = await get_breastcancer_source_id()
    if not source_id:
        print("❌ ERROR: breastcancer.org source not found in news_sources table")
        return []

    # Scrape content with Playwright (for JavaScript rendering)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            try:
                await page.goto(URL)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                html = await page.content()
                print(
                    f"✅ Successfully fetched HTML with Playwright ({len(html)} chars)"
                )
            except Exception as e:
                print(f"❌ Error loading page {URL}: {e}")
                await browser.close()
                return []
            finally:
                await browser.close()
    except Exception as e:
        print(f"❌ Failed to retrieve content from {URL}: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    inserted_ids = []
    articles_processed = 0
    articles_inserted = 0
    articles_duplicated = 0

    print(f"📄 Parsing articles...")

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/research-news/") and "topic/" not in href.lower():
            articles_processed += 1
            title = a_tag.get_text(strip=True)
            full_url = urljoin(BASE_URL, href)

            if not title:  # Skip empty titles
                continue

            # Extract summary
            parent = a_tag.find_parent("div")
            p = parent.find_next("p") if parent else None
            summary = p.get_text(strip=True) if p else ""

            # Extract publication date
            date: Optional[datetime] = None
            info_div = (
                parent.find_next("div", class_="Info_dateAndAuthorWrapper__M8I4F")
                if parent
                else None
            )

            if info_div:
                raw = info_div.get_text(" ", strip=True)
                date_str = raw.split("|", 1)[0].strip()
                try:
                    date = datetime.strptime(date_str, "%b %d, %Y")
                except ValueError:
                    print(f"⚠️  Date parsing failed for {full_url}: {raw}")
                    # Use current date as fallback
                    date = datetime.now(timezone.utc)
            else:
                # Use current date as fallback
                date = datetime.now(timezone.utc)

            # Calculate metadata
            content_text = f"{title} {summary}"
            content_hash = calculate_content_hash(content_text)
            word_count = count_words(content_text)

            try:
                # Check for duplicates first
                existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
                existing = await db_manager.execute_sql_one(existing_query, full_url)

                if existing:
                    articles_duplicated += 1
                    continue

                # Insert new article (using naive datetime for PostgreSQL compatibility)
                current_time = datetime.now(timezone.utc)

                insert_query = """
                    INSERT INTO articles (
                        source_id, title, url, content, summary, published_at,
                        scraped_at, language, country, processing_status,
                        content_hash, word_count
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                    RETURNING id
                """

                result = await db_manager.execute_sql_one(
                    insert_query,
                    source_id,
                    title,
                    full_url,
                    "",  # content to be filled later by full-text scraper
                    summary,
                    date,
                    current_time,
                    "en",
                    "United States",
                    "pending",
                    content_hash,
                    word_count,
                )

                if result:
                    article_id = result["id"]
                    inserted_ids.append(article_id)
                    articles_inserted += 1
                    print(f"✅ Inserted: {title[:50]}... (ID: {article_id})")

            except Exception as e:
                print(f"❌ Error inserting article {title[:50]}...: {str(e)}")
                continue

    print(f"\n🎯 Scraping completed:")
    print(f"   📊 Processed: {articles_processed}")
    print(f"   ✅ Inserted: {articles_inserted}")
    print(f"   ⚠️  Duplicated: {articles_duplicated}")
    print(f"   🆔 IDs: {inserted_ids[:5]}{'...' if len(inserted_ids) > 5 else ''}")

    return inserted_ids


# Main entry point for testing
if __name__ == "__main__":

    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_breastcancer_org_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles to PostgreSQL")
        finally:
            await close_database()

    asyncio.run(main())
