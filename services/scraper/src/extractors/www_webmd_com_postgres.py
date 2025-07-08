"""
Migrated scraper for WebMD - PostgreSQL Storage
Phase 1: Direct database storage with analytics-ready structure
"""

import asyncio
import hashlib
import os
import re
import sys
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Add project root to path for imports
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(project_root)

from services.data.database.connection import db_manager


def calculate_content_hash(content: str) -> str:
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_webmd_source_id() -> Optional[int]:
    """Get the source_id for WebMD from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE '%webmd.com%' LIMIT 1"
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


def parse_webmd_date(date_str: str) -> Optional[datetime]:
    """Parse WebMD date string with multiple format attempts"""
    if not date_str:
        return None

    # Multiple date format attempts
    formats = [
        "%B %d, %Y",  # March 15, 2025
        "%b %d, %Y",  # Mar 15, 2025
        "%B %d %Y",  # March 15 2025
        "%b %d %Y",  # Mar 15 2025
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Manual parsing as fallback
    try:
        date_parts = re.match(r"([A-Za-z]+)\s+(\d+),?\s+(\d{4})", date_str)
        if date_parts:
            month, day, year = date_parts.groups()
            months = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12,
                "Jan": 1,
                "Feb": 2,
                "Mar": 3,
                "Apr": 4,
                "May": 5,
                "Jun": 6,
                "Jul": 7,
                "Aug": 8,
                "Sep": 9,
                "Oct": 10,
                "Nov": 11,
                "Dec": 12,
            }
            month_num = months.get(month, 1)
            return datetime(int(year), month_num, int(day))
    except Exception as e:
        print(f"❌ Error parsing date '{date_str}': {e}")

    return None


async def scrape_webmd_to_postgres() -> List[int]:
    """
    Migrated WebMD scraper that stores articles directly in PostgreSQL
    Returns: List of inserted article IDs
    """
    URL = "https://www.webmd.com/breast-cancer/news-features"
    BASE_URL = "https://www.webmd.com"

    print(f"🔍 Starting scrape of {URL}")

    # Get source_id from database
    source_id = await get_webmd_source_id()
    if not source_id:
        print("❌ ERROR: WebMD source not found in news_sources table")
        return []

    # Scrape content with Playwright
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

    # WebMD specific parsing: <li> within ul.list
    for li in soup.select("ul.list > li"):
        a_tag = li.find("a", href=True, attrs={"data-id": True})
        if not a_tag:
            continue

        articles_processed += 1
        href = a_tag["href"]
        full_url = urljoin(BASE_URL, href)

        # Extract title
        title_span = a_tag.find("span", class_="title")
        title = title_span.get_text(strip=True) if title_span else ""

        if not title:  # Skip empty titles
            continue

        # Extract summary and date
        desc_p = a_tag.find("p", class_="desc")
        summary = ""
        date_str = ""

        if desc_p:
            date_span = desc_p.find("span", class_="tag")
            if date_span:
                raw_date = date_span.get_text(strip=True)

                # Extract date from tag
                date_match = re.search(r"([A-Za-z]+\s+\d+,\s+\d{4})", raw_date)
                if date_match:
                    date_str = date_match.group(1).strip()
                else:
                    date_match = re.search(r"([A-Za-z]+\s+\d+\s+\d{4})", raw_date)
                    if date_match:
                        date_str = date_match.group(1).strip()

                # Remove date span and get summary
                date_span.extract()
                summary = desc_p.get_text(strip=True)

        # Parse date
        date = parse_webmd_date(date_str)
        if not date:
            print(f"⚠️ Skipping article without valid date: {title[:50]}...")
            continue

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

            # Insert new article
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
            article_ids = await scrape_webmd_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles to PostgreSQL")
        finally:
            await close_database()

    asyncio.run(main())
