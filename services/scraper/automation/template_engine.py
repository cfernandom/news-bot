"""
Template engine for automated scraper generation.
Generates scraper code based on site structure and templates.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from jinja2 import DictLoader, Environment, Template

from .models import SiteStructure

logger = logging.getLogger(__name__)


def generate_date_parsing_code() -> str:
    """
    Generate comprehensive date parsing code for scrapers.
    Handles multiple date formats commonly found in news websites.
    """
    return '''
def parse_article_date(date_text: str) -> datetime:
    """
    Parse article publication date from various text formats.

    Args:
        date_text: Raw date text from website

    Returns:
        Parsed datetime object, defaults to current UTC time if parsing fails
    """
    import re
    from datetime import datetime, timezone
    from dateutil import parser as date_parser

    if not date_text or not date_text.strip():
        return datetime.now(timezone.utc)

    # Clean the date text
    date_text = date_text.strip()

    # Common date format patterns for news sites
    date_patterns = [
        # ISO formats
        (r'\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}', '%Y-%m-%dT%H:%M:%S'),
        (r'\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}', '%Y-%m-%d %H:%M:%S'),
        (r'\\d{4}-\\d{2}-\\d{2}', '%Y-%m-%d'),

        # US formats
        (r'\\d{1,2}/\\d{1,2}/\\d{4}', '%m/%d/%Y'),
        (r'\\d{1,2}-\\d{1,2}-\\d{4}', '%m-%d-%Y'),

        # European formats
        (r'\\d{1,2}\\.\\d{1,2}\\.\\d{4}', '%d.%m.%Y'),
        (r'\\d{1,2}/\\d{1,2}/\\d{4}', '%d/%m/%Y'),

        # Long formats
        (r'\\w+ \\d{1,2}, \\d{4}', '%B %d, %Y'),
        (r'\\d{1,2} \\w+ \\d{4}', '%d %B %Y'),

        # Medical/scientific formats
        (r'\\d{4} \\w+ \\d{1,2}', '%Y %B %d'),
        (r'\\w+ \\d{4}', '%B %Y'),
    ]

    # Try pattern matching first
    for pattern, format_str in date_patterns:
        if re.search(pattern, date_text):
            try:
                # Extract the matched portion
                match = re.search(pattern, date_text)
                if match:
                    date_str = match.group()
                    parsed_date = datetime.strptime(date_str, format_str)
                    # Add timezone info if missing
                    if parsed_date.tzinfo is None:
                        parsed_date = parsed_date.replace(tzinfo=timezone.utc)
                    return parsed_date
            except (ValueError, AttributeError):
                continue

    # Try dateutil parser as fallback (handles many formats automatically)
    try:
        parsed_date = date_parser.parse(date_text)
        # Ensure timezone awareness
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        return parsed_date
    except (ValueError, TypeError, AttributeError):
        pass

    # Try to extract just the date part if text contains extra content
    # Look for common date patterns in longer text
    date_in_text_patterns = [
        r'(\\d{4}-\\d{2}-\\d{2})',
        r'(\\d{1,2}/\\d{1,2}/\\d{4})',
        r'(\\w+ \\d{1,2}, \\d{4})',
        r'(\\d{1,2} \\w+ \\d{4})',
    ]

    for pattern in date_in_text_patterns:
        match = re.search(pattern, date_text)
        if match:
            try:
                extracted_date = match.group(1)
                parsed_date = date_parser.parse(extracted_date)
                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=timezone.utc)
                return parsed_date
            except (ValueError, TypeError, AttributeError):
                continue

    # If all parsing fails, return current time with a warning log
    logger.warning(f"Could not parse date text: '{date_text}', using current time")
    return datetime.now(timezone.utc)
'''


class ScraperTemplateEngine:
    """
    Template engine for generating scrapers based on site structure.
    Uses Jinja2 templates with predefined patterns for different CMS types.
    """

    def __init__(self):
        self.templates = self._load_templates()
        self.jinja_env = Environment(loader=DictLoader(self.templates))
        self.last_template_used = "none"
        self.date_parsing_code = generate_date_parsing_code()

    def _load_templates(self) -> Dict[str, str]:
        """
        Load scraper templates for different CMS types.

        Returns:
            Dictionary of template names to template content
        """
        return {
            "wordpress": self._get_wordpress_template(),
            "drupal": self._get_drupal_template(),
            "custom_medical": self._get_custom_medical_template(),
            "news_site": self._get_news_site_template(),
            "generic_article": self._get_generic_article_template(),
            "generic": self._get_generic_template(),
        }

    def _get_wordpress_template(self) -> str:
        """WordPress scraper template."""
        return '''"""
Generated WordPress scraper for {{ domain }}.
Auto-generated on {{ generation_date }} by PreventIA automation system.
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
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_{{ domain_safe }}_source_id() -> Optional[int]:
    """Get the source_id for {{ domain }} from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE %s LIMIT 1"
    result = await db_manager.execute_sql_one(query, f"%{{ domain }}%")
    return result["id"] if result else None


async def scrape_{{ domain_safe }}_to_postgres() -> List[int]:
    """
    WordPress scraper for {{ domain }}
    Returns: List of inserted article IDs
    """
    BASE_URL = "https://{{ domain }}"
    ARTICLE_LIST_URL = "{{ article_list_url }}"

    print(f"🔍 Starting scrape of {ARTICLE_LIST_URL}")

    # Get source_id from database
    source_id = await get_{{ domain_safe }}_source_id()
    if not source_id:
        print(f"❌ ERROR: {{ domain }} source not found in news_sources table")
        return []

    # Compliance settings
    CRAWL_DELAY = {{ crawl_delay }}
    MAX_ARTICLES = {{ max_articles }}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set user agent
            await page.set_extra_http_headers({
                "User-Agent": "PreventIA-NewsBot/1.0 (Academic Research)"
            })

            try:
                # Load article list page
                await page.goto(ARTICLE_LIST_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)  # Wait for dynamic content

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")

                # Extract article links using WordPress patterns
                article_links = []

                # WordPress-specific selectors
                selectors = [
                    "{{ article_link_selector }}",
                    ".post-title a",
                    ".entry-title a",
                    "h2.post-title a",
                    "h3.post-title a"
                ]

                for selector in selectors:
                    if selector and selector != "":
                        elements = soup.select(selector)
                        for element in elements:
                            if element.get("href"):
                                article_links.append({
                                    "title": element.get_text(strip=True),
                                    "url": urljoin(BASE_URL, element["href"])
                                })

                # Remove duplicates
                seen_urls = set()
                unique_articles = []
                for article in article_links:
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        unique_articles.append(article)

                # Limit articles
                articles_to_process = unique_articles[:MAX_ARTICLES]

                print(f"📄 Found {len(articles_to_process)} articles to process")

                inserted_ids = []
                articles_processed = 0
                articles_inserted = 0
                articles_duplicated = 0

                # Process each article
                for article_info in articles_to_process:
                    articles_processed += 1

                    try:
                        # Navigate to article page
                        await page.goto(article_info["url"], wait_until="domcontentloaded")
                        await page.wait_for_timeout(CRAWL_DELAY * 1000)  # Respect crawl delay

                        article_html = await page.content()
                        article_soup = BeautifulSoup(article_html, "html.parser")

                        # Extract article data
                        title = article_info["title"]
                        if not title:
                            title_elem = article_soup.select_one("{{ title_selector }}")
                            title = title_elem.get_text(strip=True) if title_elem else ""

                        # Extract content summary
                        summary = ""
                        content_elem = article_soup.select_one("{{ content_selector }}")
                        if content_elem:
                            # Get first paragraph as summary
                            first_p = content_elem.find("p")
                            if first_p:
                                summary = first_p.get_text(strip=True)[:500]

                        # Extract publication date
                        date = datetime.now(timezone.utc)  # Default to current time
                        date_elem = article_soup.select_one("{{ date_selector }}")
                        if date_elem:
                            date_text = date_elem.get_text(strip=True)
                            date = parse_article_date(date_text)

                        # Calculate metadata
                        content_text = f"{title} {summary}"
                        content_hash = calculate_content_hash(content_text)
                        word_count = count_words(content_text)

                        # Check for duplicates
                        existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
                        existing = await db_manager.execute_sql_one(existing_query, article_info["url"])

                        if existing:
                            articles_duplicated += 1
                            continue

                        # Insert new article
                        current_time = datetime.utcnow()

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
                            article_info["url"],
                            "",  # content to be filled later
                            summary,
                            date,
                            current_time,
                            "{{ language }}",
                            "{{ country }}",
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
                        print(f"❌ Error processing article {article_info['url']}: {str(e)}")
                        continue

                print(f"\\n🎯 Scraping completed:")
                print(f"   📊 Processed: {articles_processed}")
                print(f"   ✅ Inserted: {articles_inserted}")
                print(f"   ⚠️  Duplicated: {articles_duplicated}")
                print(f"   🆔 IDs: {inserted_ids[:5]}{'...' if len(inserted_ids) > 5 else ''}")

                return inserted_ids

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Failed to scrape {{ domain }}: {e}")
        return []


# Main entry point for testing
if __name__ == "__main__":
    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_{{ domain_safe }}_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles from {{ domain }}")
        finally:
            await close_database()

    asyncio.run(main())
'''

    def _get_drupal_template(self) -> str:
        """Drupal scraper template."""
        return '''"""
Generated Drupal scraper for {{ domain }}.
Auto-generated on {{ generation_date }} by PreventIA automation system.
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
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_{{ domain_safe }}_source_id() -> Optional[int]:
    """Get the source_id for {{ domain }} from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE %s LIMIT 1"
    result = await db_manager.execute_sql_one(query, f"%{{ domain }}%")
    return result["id"] if result else None


async def scrape_{{ domain_safe }}_to_postgres() -> List[int]:
    """
    Drupal scraper for {{ domain }}
    Returns: List of inserted article IDs
    """
    BASE_URL = "https://{{ domain }}"
    ARTICLE_LIST_URL = "{{ article_list_url }}"

    print(f"🔍 Starting scrape of {ARTICLE_LIST_URL}")

    # Get source_id from database
    source_id = await get_{{ domain_safe }}_source_id()
    if not source_id:
        print(f"❌ ERROR: {{ domain }} source not found in news_sources table")
        return []

    # Compliance settings
    CRAWL_DELAY = {{ crawl_delay }}
    MAX_ARTICLES = {{ max_articles }}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set user agent
            await page.set_extra_http_headers({
                "User-Agent": "PreventIA-NewsBot/1.0 (Academic Research)"
            })

            try:
                # Load article list page
                await page.goto(ARTICLE_LIST_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)  # Wait for dynamic content

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")

                # Extract article links using Drupal patterns
                article_links = []

                # Drupal-specific selectors
                selectors = [
                    "{{ article_link_selector }}",
                    ".node-title a",
                    ".field-name-title a",
                    ".view-content .views-row a",
                    ".item-list .node a"
                ]

                for selector in selectors:
                    if selector and selector != "":
                        elements = soup.select(selector)
                        for element in elements:
                            if element.get("href"):
                                article_links.append({
                                    "title": element.get_text(strip=True),
                                    "url": urljoin(BASE_URL, element["href"])
                                })

                # Remove duplicates
                seen_urls = set()
                unique_articles = []
                for article in article_links:
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        unique_articles.append(article)

                # Limit articles
                articles_to_process = unique_articles[:MAX_ARTICLES]

                print(f"📄 Found {len(articles_to_process)} articles to process")

                inserted_ids = []
                articles_processed = 0
                articles_inserted = 0
                articles_duplicated = 0

                # Process each article
                for article_info in articles_to_process:
                    articles_processed += 1

                    try:
                        # Navigate to article page
                        await page.goto(article_info["url"], wait_until="domcontentloaded")
                        await page.wait_for_timeout(CRAWL_DELAY * 1000)  # Respect crawl delay

                        article_html = await page.content()
                        article_soup = BeautifulSoup(article_html, "html.parser")

                        # Extract article data
                        title = article_info["title"]
                        if not title:
                            title_elem = article_soup.select_one("{{ title_selector }}")
                            title = title_elem.get_text(strip=True) if title_elem else ""

                        # Extract content summary
                        summary = ""
                        content_elem = article_soup.select_one("{{ content_selector }}")
                        if content_elem:
                            # Get first paragraph as summary
                            first_p = content_elem.find("p")
                            if first_p:
                                summary = first_p.get_text(strip=True)[:500]

                        # Extract publication date
                        date = datetime.now(timezone.utc)  # Default to current time
                        date_elem = article_soup.select_one("{{ date_selector }}")
                        if date_elem:
                            date_text = date_elem.get_text(strip=True)
                            date = parse_article_date(date_text)

                        # Calculate metadata
                        content_text = f"{title} {summary}"
                        content_hash = calculate_content_hash(content_text)
                        word_count = count_words(content_text)

                        # Check for duplicates
                        existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
                        existing = await db_manager.execute_sql_one(existing_query, article_info["url"])

                        if existing:
                            articles_duplicated += 1
                            continue

                        # Insert new article
                        current_time = datetime.utcnow()

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
                            article_info["url"],
                            "",  # content to be filled later
                            summary,
                            date,
                            current_time,
                            "{{ language }}",
                            "{{ country }}",
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
                        print(f"❌ Error processing article {article_info['url']}: {str(e)}")
                        continue

                print(f"\\n🎯 Scraping completed:")
                print(f"   📊 Processed: {articles_processed}")
                print(f"   ✅ Inserted: {articles_inserted}")
                print(f"   ⚠️  Duplicated: {articles_duplicated}")
                print(f"   🆔 IDs: {inserted_ids[:5]}{'...' if len(inserted_ids) > 5 else ''}")

                return inserted_ids

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Failed to scrape {{ domain }}: {e}")
        return []


# Main entry point for testing
if __name__ == "__main__":
    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_{{ domain_safe }}_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles from {{ domain }}")
        finally:
            await close_database()

    asyncio.run(main())
'''

    def _get_custom_medical_template(self) -> str:
        """Custom medical site scraper template."""
        return '''"""
Generated medical site scraper for {{ domain }}.
Auto-generated on {{ generation_date }} by PreventIA automation system.
Medical content disclaimer: This is automated research data collection.
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
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_{{ domain_safe }}_source_id() -> Optional[int]:
    """Get the source_id for {{ domain }} from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE %s LIMIT 1"
    result = await db_manager.execute_sql_one(query, f"%{{ domain }}%")
    return result["id"] if result else None


async def scrape_{{ domain_safe }}_to_postgres() -> List[int]:
    """
    Medical site scraper for {{ domain }}
    Returns: List of inserted article IDs
    """
    BASE_URL = "https://{{ domain }}"
    ARTICLE_LIST_URL = "{{ article_list_url }}"

    print(f"🔍 Starting medical content scrape of {ARTICLE_LIST_URL}")

    # Get source_id from database
    source_id = await get_{{ domain_safe }}_source_id()
    if not source_id:
        print(f"❌ ERROR: {{ domain }} source not found in news_sources table")
        return []

    # Compliance settings (conservative for medical content)
    CRAWL_DELAY = {{ crawl_delay }}
    MAX_ARTICLES = {{ max_articles }}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set user agent with medical disclaimer
            await page.set_extra_http_headers({
                "User-Agent": "PreventIA-NewsBot/1.0 (Academic Medical Research)"
            })

            try:
                # Load article list page
                await page.goto(ARTICLE_LIST_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)  # Wait for dynamic content

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")

                # Extract article links using medical site patterns
                article_links = []

                # Medical site-specific selectors
                selectors = [
                    "{{ article_link_selector }}",
                    ".medical-news a",
                    ".health-article a",
                    ".news-item a",
                    ".article-title a",
                    ".health-news a"
                ]

                for selector in selectors:
                    if selector and selector != "":
                        elements = soup.select(selector)
                        for element in elements:
                            if element.get("href"):
                                article_links.append({
                                    "title": element.get_text(strip=True),
                                    "url": urljoin(BASE_URL, element["href"])
                                })

                # Remove duplicates
                seen_urls = set()
                unique_articles = []
                for article in article_links:
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        unique_articles.append(article)

                # Limit articles
                articles_to_process = unique_articles[:MAX_ARTICLES]

                print(f"📄 Found {len(articles_to_process)} medical articles to process")

                inserted_ids = []
                articles_processed = 0
                articles_inserted = 0
                articles_duplicated = 0

                # Process each article
                for article_info in articles_to_process:
                    articles_processed += 1

                    try:
                        # Navigate to article page
                        await page.goto(article_info["url"], wait_until="domcontentloaded")
                        await page.wait_for_timeout(CRAWL_DELAY * 1000)  # Respect crawl delay

                        article_html = await page.content()
                        article_soup = BeautifulSoup(article_html, "html.parser")

                        # Extract article data
                        title = article_info["title"]
                        if not title:
                            title_elem = article_soup.select_one("{{ title_selector }}")
                            title = title_elem.get_text(strip=True) if title_elem else ""

                        # Extract content summary
                        summary = ""
                        content_elem = article_soup.select_one("{{ content_selector }}")
                        if content_elem:
                            # Get first paragraph as summary
                            first_p = content_elem.find("p")
                            if first_p:
                                summary = first_p.get_text(strip=True)[:500]

                        # Extract publication date
                        date = datetime.now(timezone.utc)  # Default to current time
                        date_elem = article_soup.select_one("{{ date_selector }}")
                        if date_elem:
                            date_text = date_elem.get_text(strip=True)
                            date = parse_article_date(date_text)

                        # Calculate metadata
                        content_text = f"{title} {summary}"
                        content_hash = calculate_content_hash(content_text)
                        word_count = count_words(content_text)

                        # Check for duplicates
                        existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
                        existing = await db_manager.execute_sql_one(existing_query, article_info["url"])

                        if existing:
                            articles_duplicated += 1
                            continue

                        # Insert new article
                        current_time = datetime.utcnow()

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
                            article_info["url"],
                            "",  # content to be filled later
                            summary,
                            date,
                            current_time,
                            "{{ language }}",
                            "{{ country }}",
                            "pending",
                            content_hash,
                            word_count,
                        )

                        if result:
                            article_id = result["id"]
                            inserted_ids.append(article_id)
                            articles_inserted += 1
                            print(f"✅ Inserted medical article: {title[:50]}... (ID: {article_id})")

                    except Exception as e:
                        print(f"❌ Error processing medical article {article_info['url']}: {str(e)}")
                        continue

                print(f"\\n🎯 Medical content scraping completed:")
                print(f"   📊 Processed: {articles_processed}")
                print(f"   ✅ Inserted: {articles_inserted}")
                print(f"   ⚠️  Duplicated: {articles_duplicated}")
                print(f"   🆔 IDs: {inserted_ids[:5]}{'...' if len(inserted_ids) > 5 else ''}")

                return inserted_ids

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Failed to scrape medical content from {{ domain }}: {e}")
        return []


# Main entry point for testing
if __name__ == "__main__":
    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_{{ domain_safe }}_to_postgres()
            print(f"✅ Scraped {len(article_ids)} medical articles from {{ domain }}")
        finally:
            await close_database()

    asyncio.run(main())
'''

    def _get_news_site_template(self) -> str:
        """News site scraper template."""
        return (
            self._get_generic_template()
            .replace("Generic site scraper", "News site scraper")
            .replace("generic site", "news site")
        )

    def _get_generic_article_template(self) -> str:
        """Generic article-based site scraper template."""
        return (
            self._get_generic_template()
            .replace("Generic site scraper", "Article-based site scraper")
            .replace("generic site", "article-based site")
        )

    def _get_generic_template(self) -> str:
        """Generic scraper template."""
        return '''"""
Generated generic site scraper for {{ domain }}.
Auto-generated on {{ generation_date }} by PreventIA automation system.
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
    """Calculate SHA-256 hash for duplicate detection"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def count_words(text: str) -> int:
    """Count words in text for analytics"""
    return len(text.split()) if text else 0


async def get_{{ domain_safe }}_source_id() -> Optional[int]:
    """Get the source_id for {{ domain }} from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE %s LIMIT 1"
    result = await db_manager.execute_sql_one(query, f"%{{ domain }}%")
    return result["id"] if result else None


async def scrape_{{ domain_safe }}_to_postgres() -> List[int]:
    """
    Generic site scraper for {{ domain }}
    Returns: List of inserted article IDs
    """
    BASE_URL = "https://{{ domain }}"
    ARTICLE_LIST_URL = "{{ article_list_url }}"

    print(f"🔍 Starting scrape of {ARTICLE_LIST_URL}")

    # Get source_id from database
    source_id = await get_{{ domain_safe }}_source_id()
    if not source_id:
        print(f"❌ ERROR: {{ domain }} source not found in news_sources table")
        return []

    # Compliance settings
    CRAWL_DELAY = {{ crawl_delay }}
    MAX_ARTICLES = {{ max_articles }}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set user agent
            await page.set_extra_http_headers({
                "User-Agent": "PreventIA-NewsBot/1.0 (Academic Research)"
            })

            try:
                # Load article list page
                await page.goto(ARTICLE_LIST_URL, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)  # Wait for dynamic content

                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")

                # Extract article links using generic patterns
                article_links = []

                # Generic selectors
                selectors = [
                    "{{ article_link_selector }}",
                    "article a",
                    ".article a",
                    ".post a",
                    ".news-item a",
                    "h2 a",
                    "h3 a"
                ]

                for selector in selectors:
                    if selector and selector != "":
                        elements = soup.select(selector)
                        for element in elements:
                            if element.get("href"):
                                article_links.append({
                                    "title": element.get_text(strip=True),
                                    "url": urljoin(BASE_URL, element["href"])
                                })

                # Remove duplicates
                seen_urls = set()
                unique_articles = []
                for article in article_links:
                    if article["url"] not in seen_urls:
                        seen_urls.add(article["url"])
                        unique_articles.append(article)

                # Limit articles
                articles_to_process = unique_articles[:MAX_ARTICLES]

                print(f"📄 Found {len(articles_to_process)} articles to process")

                inserted_ids = []
                articles_processed = 0
                articles_inserted = 0
                articles_duplicated = 0

                # Process each article
                for article_info in articles_to_process:
                    articles_processed += 1

                    try:
                        # Navigate to article page
                        await page.goto(article_info["url"], wait_until="domcontentloaded")
                        await page.wait_for_timeout(CRAWL_DELAY * 1000)  # Respect crawl delay

                        article_html = await page.content()
                        article_soup = BeautifulSoup(article_html, "html.parser")

                        # Extract article data
                        title = article_info["title"]
                        if not title:
                            title_elem = article_soup.select_one("{{ title_selector }}")
                            title = title_elem.get_text(strip=True) if title_elem else ""

                        # Extract content summary
                        summary = ""
                        content_elem = article_soup.select_one("{{ content_selector }}")
                        if content_elem:
                            # Get first paragraph as summary
                            first_p = content_elem.find("p")
                            if first_p:
                                summary = first_p.get_text(strip=True)[:500]

                        # Extract publication date
                        date = datetime.now(timezone.utc)  # Default to current time
                        date_elem = article_soup.select_one("{{ date_selector }}")
                        if date_elem:
                            date_text = date_elem.get_text(strip=True)
                            date = parse_article_date(date_text)

                        # Calculate metadata
                        content_text = f"{title} {summary}"
                        content_hash = calculate_content_hash(content_text)
                        word_count = count_words(content_text)

                        # Check for duplicates
                        existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
                        existing = await db_manager.execute_sql_one(existing_query, article_info["url"])

                        if existing:
                            articles_duplicated += 1
                            continue

                        # Insert new article
                        current_time = datetime.utcnow()

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
                            article_info["url"],
                            "",  # content to be filled later
                            summary,
                            date,
                            current_time,
                            "{{ language }}",
                            "{{ country }}",
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
                        print(f"❌ Error processing article {article_info['url']}: {str(e)}")
                        continue

                print(f"\\n🎯 Scraping completed:")
                print(f"   📊 Processed: {articles_processed}")
                print(f"   ✅ Inserted: {articles_inserted}")
                print(f"   ⚠️  Duplicated: {articles_duplicated}")
                print(f"   🆔 IDs: {inserted_ids[:5]}{'...' if len(inserted_ids) > 5 else ''}")

                return inserted_ids

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Failed to scrape {{ domain }}: {e}")
        return []


# Main entry point for testing
if __name__ == "__main__":
    async def main():
        from services.data.database.connection import close_database, init_database

        try:
            await init_database()
            article_ids = await scrape_{{ domain_safe }}_to_postgres()
            print(f"✅ Scraped {len(article_ids)} articles from {{ domain }}")
        finally:
            await close_database()

    asyncio.run(main())
'''

    async def generate_scraper(
        self, site_structure: SiteStructure, source_config: Dict[str, Any] = None
    ) -> str:
        """
        Generate scraper code based on site structure and configuration.

        Args:
            site_structure: Analyzed site structure
            source_config: Optional source configuration

        Returns:
            Generated scraper code
        """
        if source_config is None:
            source_config = {}

        logger.info(f"⚙️ Generating scraper for {site_structure.domain}")
        logger.info(f"CMS Type: {site_structure.cms_type}")

        # Select appropriate template
        template_name = self._select_template(site_structure)
        self.last_template_used = template_name

        # Prepare template variables
        template_vars = self._prepare_template_variables(site_structure, source_config)

        # Generate scraper code
        template = self.jinja_env.get_template(template_name)
        scraper_code = template.render(**template_vars)

        # Prepend date parsing function to the generated code
        full_scraper_code = self.date_parsing_code + "\n\n" + scraper_code

        logger.info(f"✅ Generated scraper using template: {template_name}")

        return full_scraper_code

    def _select_template(self, site_structure: SiteStructure) -> str:
        """
        Select appropriate template based on site structure.

        Args:
            site_structure: Analyzed site structure

        Returns:
            Template name
        """
        cms_type = site_structure.cms_type

        # Direct mapping for known CMS types
        if cms_type in self.templates:
            return cms_type

        # Fallback logic
        if cms_type == "unknown":
            if site_structure.complexity_score > 0.7:
                return "generic"
            else:
                return "generic_article"

        # Default to generic
        return "generic"

    def _prepare_template_variables(
        self, site_structure: SiteStructure, source_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare variables for template rendering.

        Args:
            site_structure: Analyzed site structure
            source_config: Source configuration

        Returns:
            Template variables dictionary
        """
        domain = site_structure.domain
        domain_safe = domain.replace(".", "_").replace("-", "_")

        # Extract selectors from site structure
        selectors = site_structure.detected_selectors
        article_patterns = site_structure.article_patterns

        # Determine article list URL
        article_list_url = self._determine_article_list_url(
            site_structure, source_config
        )

        # Determine selectors
        article_link_selector = self._determine_article_link_selector(
            selectors, article_patterns
        )
        title_selector = self._determine_title_selector(selectors, article_patterns)
        content_selector = self._determine_content_selector(selectors, article_patterns)
        date_selector = self._determine_date_selector(selectors, article_patterns)

        # Determine crawl delay
        crawl_delay = source_config.get("crawl_delay", 2)
        if site_structure.complexity_score > 0.7:
            crawl_delay += 1

        # Determine max articles
        max_articles = source_config.get("max_articles", 30)

        # Language and country
        language = source_config.get("language", "en")
        country = source_config.get("country", "US")

        return {
            "domain": domain,
            "domain_safe": domain_safe,
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "article_list_url": article_list_url,
            "article_link_selector": article_link_selector,
            "title_selector": title_selector,
            "content_selector": content_selector,
            "date_selector": date_selector,
            "crawl_delay": crawl_delay,
            "max_articles": max_articles,
            "language": language,
            "country": country,
            "cms_type": site_structure.cms_type,
            "complexity_score": site_structure.complexity_score,
            "requires_playwright": site_structure.requires_playwright,
        }

    def _determine_article_list_url(
        self, site_structure: SiteStructure, source_config: Dict[str, Any]
    ) -> str:
        """Determine the article list URL."""
        if "article_list_url" in source_config:
            return source_config["article_list_url"]

        # Check if we found one during analysis
        if "article_list_url" in site_structure.article_patterns:
            return site_structure.article_patterns["article_list_url"]

        # Default options
        domain = site_structure.domain
        default_paths = ["/news", "/articles", "/blog", "/stories", ""]

        # Return first default path
        return f"https://{domain}{default_paths[0]}"

    def _determine_article_link_selector(
        self, selectors: Dict[str, List[str]], patterns: Dict[str, str]
    ) -> str:
        """Determine the article link selector."""
        if "article_links" in selectors and selectors["article_links"]:
            return selectors["article_links"][0]

        # Check patterns
        for key, value in patterns.items():
            if "article_list_selector" in key:
                return value

        # Default
        return "article a, .article a, .post a"

    def _determine_title_selector(
        self, selectors: Dict[str, List[str]], patterns: Dict[str, str]
    ) -> str:
        """Determine the title selector."""
        if "title_selectors" in selectors and selectors["title_selectors"]:
            return selectors["title_selectors"][0]

        # Check patterns
        for key, value in patterns.items():
            if "title_" in key:
                return value

        # Default
        return "h1, .title, .article-title"

    def _determine_content_selector(
        self, selectors: Dict[str, List[str]], patterns: Dict[str, str]
    ) -> str:
        """Determine the content selector."""
        if "content_selectors" in selectors and selectors["content_selectors"]:
            return selectors["content_selectors"][0]

        # Check patterns
        for key, value in patterns.items():
            if "content_" in key:
                return value

        # Default
        return ".content, .article-content, .post-content"

    def _determine_date_selector(
        self, selectors: Dict[str, List[str]], patterns: Dict[str, str]
    ) -> str:
        """Determine the date selector."""
        if "date_selectors" in selectors and selectors["date_selectors"]:
            return selectors["date_selectors"][0]

        # Check patterns
        for key, value in patterns.items():
            if "date_" in key:
                return value

        # Default
        return "time, .date, .publish-date"
