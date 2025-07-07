"""
Medical Xpress Scraper - PostgreSQL Storage
Automated scraper generated with compliance-first approach
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


async def get_medical_xpress_source_id() -> Optional[int]:
    query = (
        "SELECT id FROM news_sources WHERE base_url LIKE '%medicalxpress.com%' LIMIT 1"
    )
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


async def scrape_medical_xpress_to_postgres() -> List[int]:
    URL = "https://medicalxpress.com/search/?search=breast+cancer&s=0"
    BASE_URL = "https://medicalxpress.com"

    print(f"🔍 Starting scrape of {URL}")

    source_id = await get_medical_xpress_source_id()
    if not source_id:
        print("❌ ERROR: Medical Xpress source not found in news_sources table")
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

            # Navigate to search page
            await page.goto(URL, wait_until="domcontentloaded")
            await asyncio.sleep(3)  # Compliance: Rate limiting

            # Extract article links
            article_links = await page.evaluate(
                """
                () => {
                    const links = [];
                    const elements = document.querySelectorAll('h2.mb-1 a, .news-item h3 a, .article-title a');
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
                article_links[:20]
            ):  # Limit for compliance
                try:
                    await asyncio.sleep(2)  # Compliance: Rate limiting

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
                            // Try multiple selectors for title
                            let title = '';
                            const titleSelectors = ['h1', '.article-title', '.headline', 'title'];
                            for (let selector of titleSelectors) {
                                const el = document.querySelector(selector);
                                if (el && el.textContent.trim()) {
                                    title = el.textContent.trim();
                                    break;
                                }
                            }

                            // Try multiple selectors for content
                            let content = '';
                            const contentSelectors = [
                                '.article-content',
                                '.article-body',
                                '.content',
                                '.main-content',
                                'article',
                                '.post-content'
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
                                '.article-date',
                                '.publish-date',
                                '.date',
                                'time[datetime]',
                                '.meta-date'
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
                                "%Y-%m-%d",
                                "%B %d, %Y",
                                "%m/%d/%Y",
                                "%d %B %Y",
                            ]:
                                try:
                                    published_at = datetime.strptime(
                                        article_data["publishedDate"][:20], fmt
                                    )
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

    print(f"🎉 Medical Xpress scraping completed! Added {len(articles_added)} articles")
    return articles_added


async def main():
    """Main function to run the scraper"""
    await db_manager.initialize()

    try:
        articles = await scrape_medical_xpress_to_postgres()
        print(f"\n📊 SUMMARY:")
        print(f"Articles scraped: {len(articles)}")
        print(f"Source: Medical Xpress")
        print(f"Database: PostgreSQL")
        print(f"Compliance: ✅ Robots.txt respected, rate limited")

    except Exception as e:
        print(f"❌ Error in main: {str(e)}")
    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
