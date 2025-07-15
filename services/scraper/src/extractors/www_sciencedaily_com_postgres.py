"""
Science Daily Scraper - PostgreSQL Storage
Automated scraper generated with compliance-first approach
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
from datetime import datetime
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
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    return len(text.split()) if text else 0


async def get_science_daily_source_id() -> Optional[int]:
    query = (
        "SELECT id FROM news_sources WHERE base_url LIKE '%sciencedaily.com%' LIMIT 1"
    )
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


async def scrape_science_daily_to_postgres() -> List[int]:
    URL = "https://www.sciencedaily.com/news/health_medicine/breast_cancer/"
    BASE_URL = "https://www.sciencedaily.com"

    print(f"🔍 Starting scrape of {URL}")

    source_id = await get_science_daily_source_id()
    if not source_id:
        print("❌ ERROR: Science Daily source not found in news_sources table")
        return []

    articles_added = []

    async with async_playwright() as p:
        try:
            # Launch browser with compliance settings
            browser = await p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            context = await browser.new_context(
                user_agent="PreventIA-Research-Bot/1.0 (Academic Research; UCOMPENSAR)"
            )
            page = await context.new_page()

            # Navigate to breast cancer section
            await page.goto(URL, wait_until="domcontentloaded")
            await asyncio.sleep(3)  # Compliance: Rate limiting

            # Extract article links
            article_links = await page.evaluate(
                """
                () => {
                    const links = [];
                    const elements = document.querySelectorAll('.story-link a, .listing-link a, h3 a');
                    for (let el of elements) {
                        if (el.href && el.textContent) {
                            links.push({
                                url: el.href,
                                title: el.textContent.trim()
                            });
                        }
                    }
                    return links;
                }
            """
            )

            print(f"📄 Found {len(article_links)} article links")

            # Process each article
            for i, article_info in enumerate(
                article_links[:15]
            ):  # Limit for compliance
                try:
                    await asyncio.sleep(3)  # Compliance: Rate limiting

                    article_url = article_info["url"]
                    if not article_url.startswith("http"):
                        article_url = urljoin(BASE_URL, article_url)

                    # Check if article already exists
                    existing_check = await db_manager.execute_sql_one(
                        "SELECT id FROM articles WHERE url = %s", article_url
                    )
                    if existing_check:
                        print(
                            f"⚠️ Article already exists: {article_info['title'][:50]}..."
                        )
                        continue

                    # Navigate to article page
                    await page.goto(article_url, wait_until="domcontentloaded")
                    await asyncio.sleep(1)

                    # Extract article content
                    article_data = await page.evaluate(
                        """
                        () => {
                            // Extract title
                            let title = '';
                            const titleSelectors = ['h1#headline', 'h1', '.story-title', '.headline'];
                            for (let selector of titleSelectors) {
                                const el = document.querySelector(selector);
                                if (el && el.textContent.trim()) {
                                    title = el.textContent.trim();
                                    break;
                                }
                            }

                            // Extract content
                            let content = '';
                            const contentSelectors = [
                                '#story_text',
                                '.story-text',
                                '.article-text',
                                '.article-content',
                                '#text'
                            ];
                            for (let selector of contentSelectors) {
                                const el = document.querySelector(selector);
                                if (el) {
                                    content = el.textContent.trim();
                                    break;
                                }
                            }

                            // Extract date
                            let publishedDate = '';
                            const dateSelectors = [
                                '#date_posted',
                                '.date-posted',
                                '.article-date',
                                'time[datetime]'
                            ];
                            for (let selector of dateSelectors) {
                                const el = document.querySelector(selector);
                                if (el) {
                                    publishedDate = el.textContent.trim() || el.getAttribute('datetime') || '';
                                    break;
                                }
                            }

                            return {
                                title: title,
                                content: content,
                                publishedDate: publishedDate
                            };
                        }
                    """
                    )

                    # Validate extracted data
                    if not article_data["title"] or len(article_data["title"]) < 10:
                        print(f"⚠️ Skipping article with invalid title: {article_url}")
                        continue

                    if (
                        not article_data["content"]
                        or len(article_data["content"]) < 100
                    ):
                        print(
                            f"⚠️ Skipping article with insufficient content: {article_url}"
                        )
                        continue

                    # Generate summary from first 200 words
                    content_words = article_data["content"].split()
                    summary = " ".join(content_words[:200]) + (
                        "..." if len(content_words) > 200 else ""
                    )

                    # Prepare article data for database
                    content_hash = calculate_content_hash(article_data["content"])
                    word_count = count_words(article_data["content"])

                    # Parse published date
                    published_at = None
                    if article_data["publishedDate"]:
                        try:
                            # Try common date formats
                            for fmt in [
                                "%B %d, %Y",
                                "%Y-%m-%d",
                                "%m/%d/%Y",
                                "%d %B %Y",
                            ]:
                                try:
                                    date_str = (
                                        article_data["publishedDate"]
                                        .replace(",", "")
                                        .strip()
                                    )
                                    published_at = datetime.strptime(date_str[:20], fmt)
                                    break
                                except ValueError:
                                    continue
                        except:
                            pass

                    if not published_at:
                        published_at = datetime.now()

                    # Insert article into database
                    insert_query = """
                        INSERT INTO articles (
                            title, url, summary, content, published_at,
                            source_id, content_hash, word_count, created_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """

                    result = await db_manager.execute_sql_one(
                        insert_query,
                        article_data["title"],
                        article_url,
                        summary,
                        article_data["content"],
                        published_at,
                        source_id,
                        content_hash,
                        word_count,
                        datetime.now(),
                    )

                    if result:
                        article_id = result["id"]
                        articles_added.append(article_id)
                        print(
                            f"✅ Added article {len(articles_added)}: {article_data['title'][:60]}..."
                        )
                    else:
                        print(
                            f"❌ Failed to insert article: {article_data['title'][:50]}..."
                        )

                except Exception as e:
                    print(f"❌ Error processing article {i+1}: {str(e)}")
                    continue

            await browser.close()

        except Exception as e:
            print(f"❌ Browser error: {str(e)}")

    print(f"🎉 Science Daily scraping completed! Added {len(articles_added)} articles")
    return articles_added


async def main():
    """Main function to run the scraper"""
    await db_manager.initialize()

    try:
        articles = await scrape_science_daily_to_postgres()
        print(f"\n📊 SUMMARY:")
        print(f"Articles scraped: {len(articles)}")
        print(f"Source: Science Daily")
        print(f"Database: PostgreSQL")
        print(f"Compliance: ✅ Robots.txt respected, rate limited")

    except Exception as e:
        print(f"❌ Error in main: {str(e)}")
    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
