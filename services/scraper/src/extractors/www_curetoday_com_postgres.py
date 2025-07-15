"""
Migrated scraper for CureToday - PostgreSQL Storage
Phase 1: Direct database storage with analytics-ready structure
"""

import asyncio
import hashlib
import os
import re
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()
from datetime import datetime, timezone
from typing import List, Optional, Set
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


async def get_curetoday_source_id() -> Optional[int]:
    """Get the source_id for CureToday from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE '%curetoday.com%' LIMIT 1"
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


def parse_curetoday_date(date_str: str) -> Optional[datetime]:
    """Parse CureToday date string with multiple format attempts"""
    if not date_str:
        return None

    # Clean date string (remove ordinals like st, nd, rd, th)
    clean_date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str.strip())

    # Multiple date format attempts
    date_formats = [
        "%B %d %Y",  # May 13 2025
        "%B %d, %Y",  # May 13, 2025
        "%b %d %Y",  # May 13 2025
        "%b %d, %Y",  # May 13, 2025
        "%m/%d/%Y",  # 05/13/2025
        "%d/%m/%Y",  # 13/05/2025
        "%Y-%m-%d",  # 2025-05-13
        "%d-%m-%Y",  # 13-05-2025
    ]

    for fmt in date_formats:
        try:
            # Return naive datetime for PostgreSQL compatibility
            parsed_date = datetime.strptime(clean_date_str, fmt)
            return parsed_date
        except ValueError:
            continue

    # Extract numbers as fallback
    numbers = re.findall(r"\d+", clean_date_str)
    if len(numbers) >= 3:
        try:
            # Assume MM/DD/YYYY or DD/MM/YYYY format
            if int(numbers[0]) > 12:  # DD/MM/YYYY
                day, month, year = int(numbers[0]), int(numbers[1]), int(numbers[2])
            else:  # MM/DD/YYYY
                month, day, year = int(numbers[0]), int(numbers[1]), int(numbers[2])

            if year < 100:
                year += 2000

            parsed_date = datetime(year, month, day)
            return parsed_date
        except (ValueError, IndexError):
            pass

    return None


async def scrape_curetoday_to_postgres() -> List[int]:
    """
    Migrated CureToday scraper that stores articles directly in PostgreSQL
    Returns: List of inserted article IDs
    """
    URL = "https://www.curetoday.com/tumor/breast"
    BASE_URL = "https://www.curetoday.com"

    print(f"🔍 Starting scrape of {URL}")

    # Get source_id from database
    source_id = await get_curetoday_source_id()
    if not source_id:
        print("❌ ERROR: CureToday source not found in news_sources table")
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

    # Track processed URLs to avoid duplicates
    processed_urls: Set[str] = set()

    print(f"📄 Parsing articles...")

    # CureToday specific parsing: div with class "w-full h-full"
    for i, article_div in enumerate(soup.find_all("div", class_="w-full h-full")):
        try:
            articles_processed += 1

            # Extract title from paragraph with specific class
            title_p = article_div.find(
                "p", class_="font-bold text-[1rem] pl-4 text-undefined"
            )
            title = ""
            href = ""

            if title_p:
                title_a = title_p.find("a", href=True)
                if title_a:
                    title = title_a.get_text(strip=True)
                    href = title_a["href"]
                else:
                    title = title_p.get_text(strip=True)

            # If no title found in paragraph, search in direct links
            if not title:
                all_links = article_div.find_all("a", href=True)
                for link in all_links:
                    link_text = link.get_text(strip=True)
                    if (
                        link_text
                        and len(link_text) > 10
                        and not link_text.lower().startswith("ryan")
                    ):
                        title = link_text
                        href = link["href"]
                        break

            if not title:
                continue

            # If no href, search for it
            if not href:
                main_link = article_div.find(
                    "a", href=lambda x: x and x.startswith("/view/")
                )
                if main_link:
                    href = main_link["href"]

            if not href:
                continue

            full_url = urljoin(BASE_URL, href)

            # Check for duplicates
            if full_url in processed_urls:
                continue

            processed_urls.add(full_url)

            # Extract summary
            summary = ""
            summary_p = article_div.find("p", class_="mt-4 text-gray-800 pl-4")
            if summary_p:
                summary = summary_p.get_text(strip=True)
            else:
                # Search for other possible summary containers
                other_p = article_div.find_all("p")
                for p in other_p:
                    text = p.get_text(strip=True)
                    if (
                        text
                        and len(text) > 30
                        and not any(
                            word in text.lower()
                            for word in ["font-bold", "ryan scott", "may", "author"]
                        )
                        and "pl-4" not in str(p.get("class", []))
                    ):
                        summary = text
                        break

            # Extract publication date with multiple attempts
            date = None

            date_span = article_div.find("span", class_="text-sm text-gray-500 pl-4")
            if date_span:
                date_str = date_span.get_text(strip=True)
                date = parse_curetoday_date(date_str)

            if not date:
                all_spans = article_div.find_all("span")
                for span in all_spans:
                    text = span.get_text(strip=True)
                    if any(
                        month in text
                        for month in [
                            "January",
                            "February",
                            "March",
                            "April",
                            "May",
                            "June",
                            "July",
                            "August",
                            "September",
                            "October",
                            "November",
                            "December",
                        ]
                    ):
                        date = parse_curetoday_date(text)
                        if date:
                            break

            if not date:
                all_text = article_div.get_text()
                date_patterns = [
                    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}",
                    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}",
                ]

                for pattern in date_patterns:
                    match = re.search(pattern, all_text)
                    if match:
                        date_str = match.group(0)
                        date = parse_curetoday_date(date_str)
                        if date:
                            break

            # Use current date as fallback if no date found
            if not date:
                date = datetime.now(timezone.utc)

            # Calculate metadata
            content_text = f"{title} {summary}"
            content_hash = calculate_content_hash(content_text)
            word_count = count_words(content_text)

            try:
                # Check for duplicates in database
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

        except Exception as e:
            print(f"❌ Error processing article {i}: {e}")
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
            article_ids = await scrape_curetoday_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles to PostgreSQL")
        finally:
            await close_database()

    asyncio.run(main())
