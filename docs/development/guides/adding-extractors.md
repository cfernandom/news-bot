---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Adding New Extractors Guide

Step-by-step guide for adding new web extractors to the PreventIA News Analytics system. This guide covers manual extractor creation, automated generation, and best practices for medical news sources.

## 🎯 Overview

### Extractor Types
1. **Basic Extractors**: Simple article list scrapers
2. **Full-text Extractors**: Complete article content extraction
3. **Automated Extractors**: AI-generated extractors
4. **Specialized Extractors**: Medical domain-specific extractors

### Development Approaches
- **Manual Development**: Traditional coding approach
- **Automated Generation**: AI-powered extractor creation
- **Template-based**: Using existing templates
- **Hybrid Approach**: Combination of manual and automated

## 🚀 Quick Start - Automated Approach

### 1. Generate Extractor Automatically
```bash
# Generate scraper for a new domain
python scripts/generate_scraper.py healthline.com

# With custom configuration
python scripts/generate_scraper.py healthline.com \
  --config '{"max_articles": 20, "language": "en"}'

# Batch generation
python scripts/generate_scraper.py \
  --batch domains.txt \
  --output-dir generated_scrapers/
```

### 2. Review Generated Code
```bash
# Check generation results
ls generated_scrapers/
cat generated_scrapers/healthline_com_scraper.py

# Review compliance status
cat generated_scrapers/healthline_com_results.json
```

### 3. Test and Deploy
```bash
# Test the generated extractor
python generated_scrapers/healthline_com_scraper.py

# Deploy to production
cp generated_scrapers/healthline_com_scraper.py \
   services/scraper/src/extractors/
```

## 🔧 Manual Extractor Development

### 1. Project Structure
```
services/scraper/src/extractors/
├── www_breastcancer_org.py          # Basic extractor
├── www_webmd_com.py                 # Basic extractor
└── template_new_extractor.py       # Template for new extractors

services/scraper/fulltext/src/extractors/
├── breastcancernow_org.py          # Full-text extractor
├── www_nature_com.py               # Full-text extractor
└── template_fulltext_extractor.py  # Full-text template
```

### 2. Basic Extractor Template

Create a new file: `services/scraper/src/extractors/www_example_com.py`

```python
"""
Basic extractor for example.com
Extracts article metadata and summaries for breast cancer news.
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

# Add project root to path
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


async def get_example_com_source_id() -> Optional[int]:
    """Get the source_id for example.com from news_sources table"""
    query = "SELECT id FROM news_sources WHERE base_url LIKE %s LIMIT 1"
    result = await db_manager.execute_sql_one(query, "%example.com%")
    return result["id"] if result else None


async def scrape_example_com_to_postgres() -> List[int]:
    """
    Scraper for example.com
    Returns: List of inserted article IDs
    """
    BASE_URL = "https://example.com"
    ARTICLE_LIST_URL = "https://example.com/health/breast-cancer"

    print(f"🔍 Starting scrape of {ARTICLE_LIST_URL}")

    # Get source_id from database
    source_id = await get_example_com_source_id()
    if not source_id:
        print("❌ Source not found in database")
        return []

    inserted_ids = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="PreventIA-NewsBot/1.0 (Academic Research)"
        )
        page = await context.new_page()

        try:
            # Navigate to article list page
            await page.goto(ARTICLE_LIST_URL, wait_until="networkidle")
            await page.wait_for_timeout(2000)  # Respect rate limiting

            # Extract article links
            article_links = await page.evaluate("""
                () => {
                    // Customize these selectors for the target site
                    const links = document.querySelectorAll('a.article-link');
                    return Array.from(links).map(link => ({
                        url: link.href,
                        title: link.textContent.trim()
                    }));
                }
            """)

            print(f"📰 Found {len(article_links)} article links")

            # Process each article
            for link_data in article_links:
                article_url = link_data['url']

                try:
                    await page.goto(article_url, wait_until="networkidle")
                    await page.wait_for_timeout(1000)  # Rate limiting

                    # Extract article data
                    article_data = await page.evaluate("""
                        () => {
                            // Customize these selectors for the target site
                            const title = document.querySelector('h1.article-title')?.textContent?.trim();
                            const content = document.querySelector('.article-content')?.textContent?.trim();
                            const dateElement = document.querySelector('time.publish-date');
                            const author = document.querySelector('.author-name')?.textContent?.trim();

                            let publishedDate = null;
                            if (dateElement) {
                                publishedDate = dateElement.getAttribute('datetime') ||
                                               dateElement.textContent.trim();
                            }

                            return {
                                title: title || '',
                                content: content || '',
                                published_date: publishedDate,
                                author: author || ''
                            };
                        }
                    """)

                    # Validate extracted data
                    if not article_data['title'] or not article_data['content']:
                        print(f"⚠️ Incomplete data for {article_url}, skipping")
                        continue

                    # Check for medical relevance (basic keyword matching)
                    content_lower = (article_data['title'] + ' ' + article_data['content']).lower()
                    medical_keywords = ['breast cancer', 'mammography', 'oncology', 'tumor', 'chemotherapy']
                    if not any(keyword in content_lower for keyword in medical_keywords):
                        print(f"⚠️ Article not medically relevant: {article_data['title'][:50]}...")
                        continue

                    # Calculate content hash for duplicate detection
                    content_hash = calculate_content_hash(article_data['content'])

                    # Check for duplicates
                    duplicate_check = await db_manager.execute_sql_one(
                        "SELECT id FROM articles WHERE content_hash = %s",
                        content_hash
                    )
                    if duplicate_check:
                        print(f"⚠️ Duplicate content found, skipping: {article_data['title'][:50]}...")
                        continue

                    # Parse published date
                    published_at = None
                    if article_data['published_date']:
                        try:
                            from dateutil import parser
                            published_at = parser.parse(article_data['published_date'])
                        except:
                            published_at = datetime.utcnow()
                    else:
                        published_at = datetime.utcnow()

                    # Prepare article for database insertion
                    article_record = {
                        'source_id': source_id,
                        'title': article_data['title'][:500],  # Truncate if too long
                        'summary': article_data['content'][:2000],  # First 2000 chars as summary
                        'content': article_data['content'],
                        'url': article_url,
                        'published_at': published_at,
                        'author': article_data['author'][:200] if article_data['author'] else None,
                        'content_hash': content_hash,
                        'word_count': count_words(article_data['content']),
                        'language': 'en',  # Adjust based on site
                        'extraction_method': 'playwright_basic',
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }

                    # Insert into database
                    insert_query = """
                        INSERT INTO articles (
                            source_id, title, summary, content, url, published_at,
                            author, content_hash, word_count, language, extraction_method,
                            created_at, updated_at
                        ) VALUES (
                            %(source_id)s, %(title)s, %(summary)s, %(content)s, %(url)s,
                            %(published_at)s, %(author)s, %(content_hash)s, %(word_count)s,
                            %(language)s, %(extraction_method)s, %(created_at)s, %(updated_at)s
                        ) RETURNING id
                    """

                    result = await db_manager.execute_sql_one(insert_query, article_record)
                    if result:
                        article_id = result['id']
                        inserted_ids.append(article_id)
                        print(f"✅ Inserted article {article_id}: {article_data['title'][:50]}...")
                    else:
                        print(f"❌ Failed to insert: {article_data['title'][:50]}...")

                except Exception as e:
                    print(f"❌ Error processing {article_url}: {str(e)}")
                    continue

        except Exception as e:
            print(f"❌ Error scraping {ARTICLE_LIST_URL}: {str(e)}")
        finally:
            await browser.close()

    print(f"🎉 Scraping completed. Inserted {len(inserted_ids)} articles")
    return inserted_ids


if __name__ == "__main__":
    asyncio.run(scrape_example_com_to_postgres())
```

### 3. Full-text Extractor Template

Create: `services/scraper/fulltext/src/extractors/example_com.py`

```python
"""
Full-text extractor for example.com
Provides complete article content extraction with advanced parsing.
"""

import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag

from ..base_extractor import BaseFullTextExtractor


class ExampleComExtractor(BaseFullTextExtractor):
    """Full-text extractor for example.com"""

    def __init__(self):
        super().__init__()
        self.domain = "example.com"
        self.base_url = "https://example.com"

        # Site-specific configuration
        self.selectors = {
            'title': 'h1.article-title',
            'content': '.article-content',
            'author': '.author-name',
            'date': 'time.publish-date',
            'tags': '.article-tags a',
            'summary': '.article-summary'
        }

        # Content cleaning rules
        self.remove_selectors = [
            '.advertisement',
            '.social-share',
            '.related-articles',
            '.comments-section'
        ]

    def can_extract(self, url: str) -> bool:
        """Check if this extractor can handle the given URL"""
        return "example.com" in url

    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract article metadata"""
        metadata = {}

        # Extract title
        title_elem = soup.select_one(self.selectors['title'])
        metadata['title'] = title_elem.get_text().strip() if title_elem else ""

        # Extract author
        author_elem = soup.select_one(self.selectors['author'])
        metadata['author'] = author_elem.get_text().strip() if author_elem else ""

        # Extract publication date
        date_elem = soup.select_one(self.selectors['date'])
        if date_elem:
            metadata['published_date'] = (
                date_elem.get('datetime') or
                date_elem.get_text().strip()
            )

        # Extract tags/categories
        tag_elements = soup.select(self.selectors['tags'])
        metadata['tags'] = [tag.get_text().strip() for tag in tag_elements]

        # Extract summary if available
        summary_elem = soup.select_one(self.selectors['summary'])
        metadata['summary'] = summary_elem.get_text().strip() if summary_elem else ""

        return metadata

    def extract_content(self, soup: BeautifulSoup, url: str) -> str:
        """Extract main article content"""
        content_elem = soup.select_one(self.selectors['content'])
        if not content_elem:
            return ""

        # Remove unwanted elements
        for selector in self.remove_selectors:
            for elem in content_elem.select(selector):
                elem.decompose()

        # Clean up the content
        content = self._clean_content(content_elem)
        return content

    def _clean_content(self, content_elem: Tag) -> str:
        """Clean and normalize article content"""
        # Remove script and style elements
        for elem in content_elem(['script', 'style']):
            elem.decompose()

        # Get text content
        text = content_elem.get_text()

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # Remove common noise patterns
        text = re.sub(r'Advertisement\s*', '', text)
        text = re.sub(r'Continue Reading Below\s*', '', text)

        return text.strip()

    def extract_images(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract article images with metadata"""
        images = []

        content_elem = soup.select_one(self.selectors['content'])
        if not content_elem:
            return images

        for img in content_elem.find_all('img'):
            img_data = {
                'src': urljoin(url, img.get('src', '')),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'caption': ''
            }

            # Look for caption in parent elements
            parent = img.parent
            if parent and parent.name in ['figure', 'div']:
                caption_elem = parent.find(['figcaption', '.caption', '.image-caption'])
                if caption_elem:
                    img_data['caption'] = caption_elem.get_text().strip()

            images.append(img_data)

        return images

    def validate_content(self, content: str, metadata: Dict) -> bool:
        """Validate extracted content quality"""
        # Check minimum content length
        if len(content.strip()) < 100:
            return False

        # Check for medical relevance
        medical_keywords = [
            'breast cancer', 'mammography', 'oncology', 'tumor',
            'chemotherapy', 'radiation', 'surgery', 'treatment'
        ]

        content_lower = (content + ' ' + metadata.get('title', '')).lower()
        if not any(keyword in content_lower for keyword in medical_keywords):
            return False

        # Check title quality
        if not metadata.get('title') or len(metadata['title']) < 10:
            return False

        return True

    def get_related_articles(self, soup: BeautifulSoup, url: str) -> List[str]:
        """Extract URLs of related articles"""
        related_urls = []

        # Look for related article sections
        related_sections = soup.select('.related-articles, .more-articles, .recommended')

        for section in related_sections:
            for link in section.find_all('a', href=True):
                related_url = urljoin(url, link['href'])
                if self.can_extract(related_url):
                    related_urls.append(related_url)

        return list(set(related_urls))  # Remove duplicates


# Register the extractor
def get_extractor():
    """Factory function to create extractor instance"""
    return ExampleComExtractor()
```

## 🎨 Advanced Customization

### 1. Site-Specific Configurations

Create configuration files for complex sites:

```python
# services/scraper/configs/example_com_config.py

EXAMPLE_COM_CONFIG = {
    'domain': 'example.com',
    'base_url': 'https://example.com',
    'crawl_delay': 2.0,
    'respect_robots_txt': True,

    'article_list_pages': [
        '/health/breast-cancer',
        '/news/oncology',
        '/research/cancer'
    ],

    'selectors': {
        'article_links': 'a.article-link, a[href*="/article/"]',
        'title': 'h1.article-title, h1.headline',
        'content': '.article-content, .post-content',
        'author': '.author-name, .byline',
        'date': 'time[datetime], .publish-date',
        'tags': '.tags a, .categories a'
    },

    'content_filters': {
        'min_word_count': 100,
        'required_keywords': ['breast cancer', 'mammography', 'oncology'],
        'exclude_patterns': [
            r'advertisement',
            r'sponsored content',
            r'continue reading'
        ]
    },

    'javascript_required': True,
    'wait_for_selector': '.article-content',
    'scroll_to_load': False
}
```

### 2. Medical Content Validation

```python
# services/scraper/validators/medical_validator.py

import re
from typing import Dict, List, Tuple

class MedicalContentValidator:
    """Validator for medical content relevance and quality"""

    def __init__(self):
        self.medical_terms = {
            'breast_cancer': [
                'breast cancer', 'mammary carcinoma', 'ductal carcinoma',
                'lobular carcinoma', 'triple negative', 'her2 positive'
            ],
            'treatments': [
                'chemotherapy', 'radiation therapy', 'immunotherapy',
                'hormone therapy', 'targeted therapy', 'surgery'
            ],
            'diagnostics': [
                'mammography', 'biopsy', 'ultrasound', 'mri',
                'ct scan', 'pet scan', 'genetic testing'
            ],
            'medical_entities': [
                'oncologist', 'radiologist', 'pathologist',
                'clinical trial', 'fda approval', 'peer review'
            ]
        }

        self.quality_indicators = [
            'clinical trial', 'peer reviewed', 'published in',
            'journal of', 'medical center', 'university',
            'fda approved', 'evidence based'
        ]

    def validate_medical_relevance(self, content: str, title: str) -> Tuple[bool, float]:
        """
        Validate if content is medically relevant to breast cancer
        Returns: (is_relevant, confidence_score)
        """
        text = (title + ' ' + content).lower()

        # Count matches in each category
        matches = {}
        for category, terms in self.medical_terms.items():
            matches[category] = sum(1 for term in terms if term in text)

        # Calculate relevance score
        total_matches = sum(matches.values())
        relevance_score = min(1.0, total_matches / 5.0)  # Normalize to 0-1

        # Require at least one breast cancer term and one other medical term
        is_relevant = (
            matches['breast_cancer'] > 0 and
            (matches['treatments'] > 0 or matches['diagnostics'] > 0)
        )

        return is_relevant, relevance_score

    def assess_content_quality(self, content: str, metadata: Dict) -> Dict:
        """Assess overall content quality for medical articles"""
        quality_metrics = {
            'word_count': len(content.split()),
            'readability_score': self._calculate_readability(content),
            'medical_authority': self._check_medical_authority(content, metadata),
            'source_credibility': self._assess_source_credibility(metadata),
            'citation_quality': self._check_citations(content)
        }

        # Calculate overall quality score
        weights = {
            'word_count': 0.1,
            'readability_score': 0.2,
            'medical_authority': 0.3,
            'source_credibility': 0.3,
            'citation_quality': 0.1
        }

        overall_score = sum(
            quality_metrics[metric] * weights[metric]
            for metric in weights
        )

        quality_metrics['overall_score'] = overall_score
        return quality_metrics

    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score for medical content"""
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())

        if sentences == 0 or words == 0:
            return 0.0

        avg_sentence_length = words / sentences

        # Medical content should be moderately complex but accessible
        # Target: 15-25 words per sentence
        if 15 <= avg_sentence_length <= 25:
            return 1.0
        elif 10 <= avg_sentence_length < 15 or 25 < avg_sentence_length <= 30:
            return 0.8
        else:
            return 0.5

    def _check_medical_authority(self, content: str, metadata: Dict) -> float:
        """Check for indicators of medical authority"""
        content_lower = content.lower()

        authority_score = 0.0

        # Check for quality indicators
        for indicator in self.quality_indicators:
            if indicator in content_lower:
                authority_score += 0.1

        # Check author credentials
        author = metadata.get('author', '').lower()
        if any(title in author for title in ['dr.', 'md', 'phd', 'professor']):
            authority_score += 0.3

        return min(1.0, authority_score)

    def _assess_source_credibility(self, metadata: Dict) -> float:
        """Assess credibility of the source"""
        # This would typically check against a database of credible sources
        # For now, use basic heuristics

        url = metadata.get('url', '').lower()

        credible_domains = [
            'nih.gov', 'cdc.gov', 'cancer.gov', 'mayo.edu',
            'harvard.edu', 'webmd.com', 'healthline.com'
        ]

        for domain in credible_domains:
            if domain in url:
                return 1.0

        # Check for academic or medical institution indicators
        if any(indicator in url for indicator in ['.edu', '.gov', 'medical', 'health']):
            return 0.8

        return 0.5

    def _check_citations(self, content: str) -> float:
        """Check for presence and quality of citations"""
        citation_patterns = [
            r'\[\d+\]',  # [1], [2], etc.
            r'\(\d{4}\)',  # (2023), (2024), etc.
            r'et al\.',  # et al.
            r'Journal of',  # Journal references
            r'doi:',  # DOI references
        ]

        citation_count = 0
        for pattern in citation_patterns:
            citation_count += len(re.findall(pattern, content))

        # Normalize citation score
        return min(1.0, citation_count / 5.0)
```

## 🧪 Testing Your Extractor

### 1. Unit Tests

Create test file: `tests/unit/test_extractors/test_example_com.py`

```python
import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

from services.scraper.fulltext.src.extractors.example_com import ExampleComExtractor


class TestExampleComExtractor:

    def setup_method(self):
        self.extractor = ExampleComExtractor()

    def test_can_extract(self):
        assert self.extractor.can_extract("https://example.com/article/123")
        assert not self.extractor.can_extract("https://other.com/article/123")

    def test_extract_metadata(self):
        html = """
        <html>
            <h1 class="article-title">Breakthrough Cancer Treatment</h1>
            <div class="author-name">Dr. Jane Smith</div>
            <time class="publish-date" datetime="2025-07-07T10:00:00Z">July 7, 2025</time>
            <div class="article-tags">
                <a href="/tag/cancer">Cancer</a>
                <a href="/tag/treatment">Treatment</a>
            </div>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')

        metadata = self.extractor.extract_metadata(soup, "https://example.com/article/123")

        assert metadata['title'] == "Breakthrough Cancer Treatment"
        assert metadata['author'] == "Dr. Jane Smith"
        assert metadata['published_date'] == "2025-07-07T10:00:00Z"
        assert "Cancer" in metadata['tags']
        assert "Treatment" in metadata['tags']

    def test_extract_content(self):
        html = """
        <html>
            <div class="article-content">
                <p>This is the main article content about breast cancer treatment.</p>
                <div class="advertisement">This is an ad</div>
                <p>More important medical information here.</p>
            </div>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')

        content = self.extractor.extract_content(soup, "https://example.com/article/123")

        assert "breast cancer treatment" in content
        assert "important medical information" in content
        assert "This is an ad" not in content  # Should be removed

    def test_validate_content(self):
        # Valid medical content
        valid_content = "This article discusses breast cancer treatment options including chemotherapy and radiation therapy."
        valid_metadata = {"title": "Breast Cancer Treatment Options"}

        assert self.extractor.validate_content(valid_content, valid_metadata) == True

        # Invalid content (too short)
        invalid_content = "Short text"
        assert self.extractor.validate_content(invalid_content, valid_metadata) == False

        # Invalid content (not medical)
        non_medical_content = "This is a long article about cooking and recipes that has nothing to do with medicine."
        assert self.extractor.validate_content(non_medical_content, valid_metadata) == False
```

### 2. Integration Tests

Create: `tests/integration/test_extractors/test_example_com_integration.py`

```python
import pytest
import asyncio
from unittest.mock import patch

from services.scraper.src.extractors.www_example_com import scrape_example_com_to_postgres


class TestExampleComIntegration:

    @pytest.mark.asyncio
    @patch('services.scraper.src.extractors.www_example_com.get_example_com_source_id')
    @patch('services.data.database.connection.db_manager.execute_sql_one')
    async def test_full_scraping_workflow(self, mock_db_execute, mock_get_source):
        # Mock database responses
        mock_get_source.return_value = 1
        mock_db_execute.side_effect = [
            None,  # Duplicate check returns None (no duplicate)
            {'id': 123}  # Insert returns new ID
        ]

        # This would require a test server or mock responses
        # For now, we'll test the structure
        with patch('playwright.async_api.async_playwright') as mock_playwright:
            # Mock Playwright browser and page
            mock_browser = Mock()
            mock_page = Mock()
            mock_context = Mock()

            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
            mock_browser.new_context.return_value = mock_context
            mock_context.new_page.return_value = mock_page

            # Mock page responses
            mock_page.evaluate.side_effect = [
                # Article links
                [{'url': 'https://example.com/article/1', 'title': 'Test Article'}],
                # Article data
                {
                    'title': 'Breast Cancer Treatment Breakthrough',
                    'content': 'This is a detailed article about new breast cancer treatment options.',
                    'published_date': '2025-07-07T10:00:00Z',
                    'author': 'Dr. Jane Smith'
                }
            ]

            # Run the scraper
            result = await scrape_example_com_to_postgres()

            # Verify the process
            assert isinstance(result, list)
            mock_page.goto.assert_called()
            mock_db_execute.assert_called()
```

### 3. Manual Testing Script

Create: `scripts/test_extractor.py`

```python
#!/usr/bin/env python3
"""
Manual testing script for individual extractors
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.scraper.src.extractors.www_example_com import scrape_example_com_to_postgres


async def test_extractor():
    """Test the extractor with database interaction"""
    print("🧪 Testing example.com extractor...")

    try:
        # Run the extractor
        result = await scrape_example_com_to_postgres()

        print(f"✅ Extractor completed successfully!")
        print(f"📊 Articles inserted: {len(result)}")
        print(f"🆔 Article IDs: {result}")

    except Exception as e:
        print(f"❌ Extractor failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_extractor())
```

## 📋 Deployment Checklist

### Pre-deployment Validation
- [ ] Compliance check passed (robots.txt, rate limiting)
- [ ] Medical relevance validation implemented
- [ ] Duplicate detection working
- [ ] Error handling comprehensive
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Manual testing completed

### Database Integration
- [ ] Source entry added to `news_sources` table
- [ ] Appropriate source_id configuration
- [ ] Database schema compatible
- [ ] Proper indexing for new source

### Performance Validation
- [ ] Response time < 2s per article
- [ ] Memory usage < 100MB
- [ ] Proper rate limiting (respects crawl-delay)
- [ ] Graceful error handling

### Production Deployment
```bash
# 1. Add to source registry
python scripts/add_news_source.py \
  --name "Example Medical News" \
  --url "https://example.com" \
  --type "news_site"

# 2. Deploy extractor
cp services/scraper/src/extractors/www_example_com.py \
   /production/services/scraper/src/extractors/

# 3. Test in production
python scripts/test_extractor_production.py example.com

# 4. Add to scheduler
python scripts/schedule_scraper.py \
  --source-id 5 \
  --frequency "daily" \
  --time "06:00"
```

## 🔍 Troubleshooting Common Issues

### Selector Not Found
```python
# Debug selectors
from bs4 import BeautifulSoup
import requests

response = requests.get("https://example.com/article/123")
soup = BeautifulSoup(response.content, 'html.parser')

# Test selectors
print("Title:", soup.select_one('h1.article-title'))
print("Content:", soup.select_one('.article-content'))

# Find alternative selectors
print("All h1 tags:", [h1.get('class') for h1 in soup.find_all('h1')])
```

### JavaScript Rendering Issues
```python
# Enable Playwright debugging
async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False, slow_mo=1000)
    # Add screenshots for debugging
    await page.screenshot(path='debug_screenshot.png')
```

### Content Quality Issues
```python
# Add content validation
def validate_extracted_content(content, title):
    issues = []

    if len(content) < 100:
        issues.append("Content too short")

    if not any(keyword in content.lower() for keyword in ['breast cancer', 'medical']):
        issues.append("Not medically relevant")

    return issues
```

## 📚 Related Documentation

- [Automated Scraper Generation](../../api/services/scraper-api.md)
- [Compliance Guidelines](../standards/compliance-standards.md)
- [Database Schema](../../architecture/data-flow.md)
- [Testing Strategy](../standards/testing-strategy.md)

---

**Extractor Development Principles:**
- **Compliance First**: Always respect robots.txt and rate limits
- **Medical Focus**: Validate content relevance to breast cancer domain
- **Quality Assurance**: Comprehensive testing and validation
- **Performance Optimized**: Efficient extraction with minimal resource usage
- **Maintainable Code**: Clear structure, documentation, and error handling

**Last Updated**: 2025-07-07
**Next Review**: 2025-10-07
**Maintainer**: Claude (Technical Director)
