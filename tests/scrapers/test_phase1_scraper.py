#!/usr/bin/env python3
"""
FASE 1 - Test de migración del primer scraper a PostgreSQL
Scraper: breastcancer.org → PostgreSQL direct storage
"""

import asyncio
import hashlib
import os
from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Cargar variables de entorno
load_dotenv()

# Importaciones locales (desde raíz del proyecto)
from services.data.database.connection import close_database, db_manager, init_database


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


async def scrape_breastcancer_org_postgres() -> List[int]:
    """
    Scraper migrado que almacena artículos directamente en PostgreSQL
    Returns: Lista de IDs de artículos insertados
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
                    date = date.replace(tzinfo=timezone.utc)
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

                # Use naive datetimes like test_database.py does
                current_time = datetime.utcnow()

                # Ensure published_at is naive datetime (no timezone)
                if date.tzinfo is not None:
                    date = date.replace(tzinfo=None)

                # Debug datetime info
                print(f"  📅 Debug - published_at: {date} (tzinfo: {date.tzinfo})")
                print(
                    f"  📅 Debug - scraped_at: {current_time} (tzinfo: {current_time.tzinfo})"
                )

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
                    date,  # Use datetime object directly
                    current_time,  # Use datetime object directly
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

                # Limit for test - max 1 article for debugging
                if articles_inserted >= 1:
                    print("🎯 Limiting to 1 article for debugging...")
                    break

            except Exception as e:
                print(f"❌ Error inserting article {title[:50]}...: {str(e)}")
                continue

    print(f"\n🎯 Scraping completed:")
    print(f"   📊 Processed: {articles_processed}")
    print(f"   ✅ Inserted: {articles_inserted}")
    print(f"   ⚠️  Duplicated: {articles_duplicated}")
    print(f"   🆔 IDs: {inserted_ids}")

    return inserted_ids


async def main():
    """Main test function"""
    print("🧪 FASE 1 - Testing breastcancer.org PostgreSQL scraper migration...")

    try:
        # Initialize database
        await init_database()
        print("✅ Database initialized")

        # Run scraper
        article_ids = await scrape_breastcancer_org_postgres()

        # Verify results
        if article_ids:
            print(
                f"\n✅ Migration test successful: {len(article_ids)} articles scraped"
            )

            # Show first article details
            first_id = article_ids[0]
            article_query = """
                SELECT a.title, a.url, a.published_at, a.summary, ns.name as source_name,
                       a.language, a.country, a.processing_status, a.word_count
                FROM articles a
                JOIN news_sources ns ON a.source_id = ns.id
                WHERE a.id = $1
            """
            article = await db_manager.execute_sql_one(article_query, first_id)
            if article:
                print(f"\n📰 Sample migrated article:")
                print(f"   Title: {article['title'][:60]}...")
                print(f"   Source: {article['source_name']}")
                print(f"   Date: {article['published_at']}")
                print(f"   Language: {article['language']}")
                print(f"   Country: {article['country']}")
                print(f"   Status: {article['processing_status']}")
                print(f"   Words: {article['word_count']}")
                print(f"   URL: {article['url']}")

            # Show total articles in database
            total_query = "SELECT COUNT(*) as total FROM articles"
            total = await db_manager.execute_sql_one(total_query)
            print(f"\n📊 Total articles in database: {total['total']}")

            print(f"\n🎯 FASE 1 COMPLETED SUCCESSFULLY!")
            print(f"   ✅ Scraper migrated to PostgreSQL")
            print(f"   ✅ {len(article_ids)} articles stored directly in database")
            print(f"   ✅ Analytics-ready data structure")
            print(f"   ✅ Ready for Phase 2 (NLP Analytics)")

        else:
            print("❌ Migration test failed: No articles scraped")
            return False

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    finally:
        await close_database()

    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🚀 Ready to proceed with remaining scrapers migration!")
    else:
        print("\n❌ Phase 1 test failed")
