"""
Nature Scraper - PostgreSQL Storage
Automated scraper generated with compliance-first approach
Special handling for academic journal content
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


async def get_nature_source_id() -> Optional[int]:
    query = "SELECT id FROM news_sources WHERE base_url LIKE '%nature.com%' LIMIT 1"
    result = await db_manager.execute_sql_one(query)
    return result["id"] if result else None


async def scrape_nature_to_postgres() -> List[int]:
    # Focus on open access content and news, not paywalled research papers
    URL = "https://www.nature.com/search?q=breast%20cancer&journal=nature"
    BASE_URL = "https://www.nature.com"

    print(f"🔍 Starting scrape of {URL}")

    source_id = await get_nature_source_id()
    if not source_id:
        print("❌ ERROR: Nature source not found in news_sources table")
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

            # Navigate to search results
            await page.goto(URL, wait_until="domcontentloaded")
            await asyncio.sleep(5)  # Compliance: Higher delay for academic publisher

            # Extract article links (focus on freely accessible content)
            article_links = await page.evaluate(
                """
                () => {
                    const links = [];
                    const elements = document.querySelectorAll('article h3 a, .result-item h3 a, .c-card__link');
                    for (let el of elements) {
                        if (el.href && el.textContent) {
                            // Only include news and openly accessible content
                            if (el.href.includes('/articles/') || el.href.includes('/news/') ||
                                el.href.includes('/d41586-') || el.textContent.toLowerCase().includes('news')) {
                                links.push({
                                    url: el.href,
                                    title: el.textContent.trim()
                                });
                            }
                        }
                    }
                    return links;
                }
            """
            )

            print(f"📄 Found {len(article_links)} article links")

            # Process each article (limited for academic publisher respect)
            for i, article_info in enumerate(article_links[:10]):  # Conservative limit
                try:
                    await asyncio.sleep(
                        5
                    )  # Compliance: Respectful delay for academic publisher

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
                    await asyncio.sleep(2)

                    # Check for paywall or access restrictions
                    has_paywall = await page.evaluate(
                        """
                        () => {
                            return document.querySelector('.paywall') ||
                                   document.querySelector('.c-article-gating') ||
                                   document.querySelector('.subscribe-prompt') ||
                                   document.textContent.includes('Subscribe to Nature') ||
                                   document.textContent.includes('This article is for subscribers only');
                        }
                    """
                    )

                    if has_paywall:
                        print(
                            f"⚠️ Skipping paywalled content: {article_info['title'][:50]}..."
                        )
                        continue

                    # Extract article content (only freely accessible parts)
                    article_data = await page.evaluate(
                        """
                        () => {
                            // Extract title
                            let title = '';
                            const titleSelectors = ['h1', '.c-article-title', '.article__title'];
                            for (let selector of titleSelectors) {
                                const el = document.querySelector(selector);
                                if (el && el.textContent.trim()) {
                                    title = el.textContent.trim();
                                    break;
                                }
                            }

                            // Extract abstract/summary only (respect copyright)
                            let content = '';
                            const abstractSelectors = [
                                '.c-article__summary',
                                '.article__abstract',
                                '.standfirst',
                                '.c-article-section--tonal .c-article-section__content p:first-child'
                            ];
                            for (let selector of abstractSelectors) {
                                const el = document.querySelector(selector);
                                if (el) {
                                    content = el.textContent.trim();
                                    break;
                                }
                            }

                            // If no abstract, get first paragraph only
                            if (!content) {
                                const firstPara = document.querySelector('.c-article-body p, .article-body p');
                                if (firstPara) {
                                    content = firstPara.textContent.trim();
                                }
                            }

                            // Extract date
                            let publishedDate = '';
                            const dateSelectors = [
                                'time[datetime]',
                                '.c-article-info-details time',
                                '.article__date'
                            ];
                            for (let selector of dateSelectors) {
                                const el = document.querySelector(selector);
                                if (el) {
                                    publishedDate = el.getAttribute('datetime') || el.textContent.trim();
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

                    if not article_data["content"] or len(article_data["content"]) < 50:
                        print(
                            f"⚠️ Skipping article with insufficient content: {article_url}"
                        )
                        continue

                    # Use content as summary (respecting copyright - only abstracts/summaries)
                    summary = article_data["content"][:500] + (
                        "..." if len(article_data["content"]) > 500 else ""
                    )

                    # Prepare article data for database
                    content_hash = calculate_content_hash(article_data["content"])
                    word_count = count_words(article_data["content"])

                    # Parse published date
                    published_at = None
                    if article_data["publishedDate"]:
                        try:
                            # Nature uses ISO format
                            if "T" in article_data["publishedDate"]:
                                published_at = datetime.fromisoformat(
                                    article_data["publishedDate"].replace("Z", "+00:00")
                                )
                            else:
                                # Try other formats
                                for fmt in ["%Y-%m-%d", "%d %B %Y", "%B %d, %Y"]:
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
                        article_data["content"],  # Only abstract/summary
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

    print(f"🎉 Nature scraping completed! Added {len(articles_added)} articles")
    return articles_added


async def main():
    """Main function to run the scraper"""
    await db_manager.initialize()

    try:
        articles = await scrape_nature_to_postgres()
        print(f"\n📊 SUMMARY:")
        print(f"Articles scraped: {len(articles)}")
        print(f"Source: Nature")
        print(f"Database: PostgreSQL")
        print(f"Compliance: ✅ Academic fair use, abstract-only, high delay respect")

    except Exception as e:
        print(f"❌ Error in main: {str(e)}")
    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
