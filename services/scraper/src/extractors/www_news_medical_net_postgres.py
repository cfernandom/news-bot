"""
Migrated scraper for News Medical - PostgreSQL Storage
Phase 1: Direct database storage with analytics-ready structure
"""

import asyncio
import hashlib
import os
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
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    return len(text.split()) if text else 0


async def get_news_medical_source_id() -> Optional[int]:
    query = (
        "SELECT id FROM news_sources WHERE base_url LIKE '%news-medical.net%' LIMIT 1"
    )
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


async def scrape_news_medical_to_postgres() -> List[int]:
    URL = "https://www.news-medical.net/condition/Breast-Cancer"
    BASE_URL = "https://www.news-medical.net"

    print(f"🔍 Starting scrape of {URL}")

    source_id = await get_news_medical_source_id()
    if not source_id:
        print("❌ ERROR: News Medical source not found in news_sources table")
        return []

    # Scrape with Playwright
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

    for article in soup.find_all("div", class_="row"):
        if not article.find("h3") or "paging" in article.get("class", []):
            continue

        articles_processed += 1

        # Extract title
        title_tag = article.find("h3").find("a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag["href"]
        full_url = urljoin(BASE_URL, href)

        # Extract summary
        summary_tag = article.find("p", class_="hidden-xs item-desc")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        # Extract date
        date_row = article.find_next_sibling("div", class_="row")
        date = None
        if date_row:
            date_span = date_row.find("span", class_="article-meta-date")
            if date_span:
                date_str = date_span.get_text(strip=True)
                try:
                    date = datetime.strptime(date_str, "%d %b %Y")
                except ValueError:
                    try:
                        date = datetime.strptime(date_str, "%d %B %Y")
                    except ValueError:
                        print(f"⚠️ Date format not recognized: {date_str}")
                        continue

        if not date:
            date = datetime.now(timezone.utc)

        # Calculate metadata
        content_text = f"{title} {summary}"
        content_hash = calculate_content_hash(content_text)
        word_count = count_words(content_text)

        try:
            # Check for duplicates
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
                "",
                summary,
                date,
                current_time,
                "en",
                "Global",
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


if __name__ == "__main__":

    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_news_medical_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles to PostgreSQL")
        finally:
            await close_database()

    asyncio.run(main())
