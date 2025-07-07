"""
Site structure analysis for automated scraper generation.
Analyzes website structure to determine optimal scraping strategy.
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from .models import SiteStructure

logger = logging.getLogger(__name__)


class SiteStructureAnalyzer:
    """
    Analyzes website structure for automated scraper generation.
    Detects CMS type, navigation patterns, and content structure.
    """

    def __init__(self):
        self.analysis_cache: Dict[str, SiteStructure] = {}

    async def analyze_site(self, domain: str) -> SiteStructure:
        """
        Comprehensive site structure analysis.

        Args:
            domain: Domain to analyze

        Returns:
            SiteStructure object with analysis results
        """
        logger.info(f"🔍 Starting site structure analysis for {domain}")

        # Check cache first
        if domain in self.analysis_cache:
            logger.info(f"📋 Using cached analysis for {domain}")
            return self.analysis_cache[domain]

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                try:
                    # Load main page
                    main_url = f"https://{domain}"
                    await page.goto(main_url, wait_until="domcontentloaded")

                    # Wait for dynamic content to load
                    await page.wait_for_timeout(3000)

                    # Get page content
                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")

                    # Perform analysis
                    cms_type = await self._detect_cms_type(page, soup)
                    navigation = await self._analyze_navigation(page, soup)
                    article_patterns = await self._detect_article_patterns(
                        page, soup, domain
                    )
                    content_structure = await self._analyze_content_structure(
                        page, soup
                    )
                    complexity_score = self._calculate_complexity_score(soup)
                    detected_selectors = await self._detect_selectors(page, soup)
                    javascript_heavy = await self._detect_javascript_dependency(page)

                    structure = SiteStructure(
                        domain=domain,
                        cms_type=cms_type,
                        navigation=navigation,
                        article_patterns=article_patterns,
                        content_structure=content_structure,
                        complexity_score=complexity_score,
                        detected_selectors=detected_selectors,
                        javascript_heavy=javascript_heavy,
                        requires_playwright=javascript_heavy or complexity_score > 0.7,
                    )

                    # Cache result
                    self.analysis_cache[domain] = structure

                    logger.info(f"✅ Site structure analysis completed for {domain}")
                    logger.info(
                        f"CMS Type: {cms_type}, Complexity: {complexity_score:.2f}"
                    )

                    return structure

                finally:
                    await browser.close()

        except Exception as e:
            logger.error(f"❌ Error analyzing site structure for {domain}: {str(e)}")
            # Return basic structure for fallback
            return SiteStructure(
                domain=domain,
                cms_type="unknown",
                navigation={},
                article_patterns={},
                content_structure={},
                complexity_score=0.5,
                detected_selectors={},
                javascript_heavy=True,
                requires_playwright=True,
            )

    async def _detect_cms_type(self, page, soup: BeautifulSoup) -> str:
        """
        Detect CMS type (WordPress, Drupal, custom, etc.).

        Args:
            page: Playwright page object
            soup: BeautifulSoup object

        Returns:
            CMS type string
        """
        try:
            # WordPress detection
            wp_indicators = [
                'meta[name="generator"][content*="WordPress"]',
                'link[href*="wp-content"]',
                'link[href*="wp-includes"]',
                'script[src*="wp-content"]',
            ]

            for indicator in wp_indicators:
                if await page.locator(indicator).count() > 0:
                    logger.info("🔍 Detected WordPress CMS")
                    return "wordpress"

            # Drupal detection
            drupal_indicators = [
                'meta[name="generator"][content*="Drupal"]',
                'link[href*="sites/default/files"]',
                'body[class*="drupal"]',
            ]

            for indicator in drupal_indicators:
                if await page.locator(indicator).count() > 0:
                    logger.info("🔍 Detected Drupal CMS")
                    return "drupal"

            # Medical/News specific CMS detection
            medical_indicators = [
                ".medical-news",
                ".health-article",
                ".news-article",
                ".medical-content",
                ".health-news",
            ]

            for indicator in medical_indicators:
                if await page.locator(indicator).count() > 0:
                    logger.info("🔍 Detected medical/news CMS")
                    return "custom_medical"

            # Check for common news site patterns
            news_patterns = soup.find_all(
                class_=lambda x: x
                and any(
                    keyword in x.lower()
                    for keyword in ["news", "article", "story", "post"]
                )
            )

            if len(news_patterns) > 5:
                logger.info("🔍 Detected news site pattern")
                return "news_site"

            # Generic detection based on structure
            if soup.find_all("article") or soup.find_all(
                class_=lambda x: x and "article" in x.lower()
            ):
                logger.info("🔍 Detected generic article-based site")
                return "generic_article"

            logger.info("🔍 Unknown CMS type")
            return "unknown"

        except Exception as e:
            logger.error(f"❌ Error detecting CMS type: {str(e)}")
            return "unknown"

    async def _analyze_navigation(self, page, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Analyze navigation structure.

        Args:
            page: Playwright page object
            soup: BeautifulSoup object

        Returns:
            Navigation structure dictionary
        """
        try:
            navigation = {
                "main_nav": [],
                "news_links": [],
                "article_links": [],
                "pagination": {},
            }

            # Find main navigation
            nav_selectors = ["nav", ".navigation", ".nav", ".menu", "header nav"]
            for selector in nav_selectors:
                nav_elements = await page.locator(selector).all()
                for nav in nav_elements:
                    links = await nav.locator("a").all()
                    nav_links = []
                    for link in links[:10]:  # Limit to first 10 links
                        try:
                            text = await link.text_content()
                            href = await link.get_attribute("href")
                            if text and href:
                                nav_links.append({"text": text.strip(), "href": href})
                        except:
                            continue
                    if nav_links:
                        navigation["main_nav"].extend(nav_links)
                        break

            # Find news/article links
            news_keywords = ["news", "article", "story", "post", "blog"]
            for keyword in news_keywords:
                links = await page.locator(f'a[href*="{keyword}"]').all()
                for link in links[:5]:  # Limit to first 5 links
                    try:
                        text = await link.text_content()
                        href = await link.get_attribute("href")
                        if text and href:
                            navigation["news_links"].append(
                                {"text": text.strip(), "href": href}
                            )
                    except:
                        continue

            # Find pagination
            pagination_selectors = [
                ".pagination",
                ".pager",
                ".page-numbers",
                ".next",
                ".previous",
            ]
            for selector in pagination_selectors:
                if await page.locator(selector).count() > 0:
                    navigation["pagination"]["detected"] = True
                    navigation["pagination"]["selector"] = selector
                    break

            return navigation

        except Exception as e:
            logger.error(f"❌ Error analyzing navigation: {str(e)}")
            return {}

    async def _detect_article_patterns(
        self, page, soup: BeautifulSoup, domain: str
    ) -> Dict[str, str]:
        """
        Detect article patterns and selectors.

        Args:
            page: Playwright page object
            soup: BeautifulSoup object
            domain: Domain being analyzed

        Returns:
            Article patterns dictionary
        """
        try:
            patterns = {}

            # Common article selectors
            article_selectors = [
                "article",
                ".article",
                ".post",
                ".news-item",
                ".story",
                ".entry",
                ".content-item",
            ]

            for selector in article_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    patterns[f"article_container_{selector}"] = selector
                    logger.info(f"🔍 Found {count} articles with selector: {selector}")

            # Title patterns
            title_selectors = [
                "h1",
                "h2",
                "h3",
                ".title",
                ".headline",
                ".article-title",
                ".post-title",
                ".entry-title",
            ]

            for selector in title_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    patterns[f"title_{selector}"] = selector

            # Content patterns
            content_selectors = [
                ".content",
                ".article-content",
                ".post-content",
                ".entry-content",
                ".article-body",
                ".story-content",
            ]

            for selector in content_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    patterns[f"content_{selector}"] = selector

            # Date patterns
            date_selectors = [
                ".date",
                ".publish-date",
                ".article-date",
                ".post-date",
                ".entry-date",
                "time",
            ]

            for selector in date_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    patterns[f"date_{selector}"] = selector

            # Try to find article list page
            try:
                # Check for common news/article list patterns
                news_urls = [
                    f"https://{domain}/news",
                    f"https://{domain}/articles",
                    f"https://{domain}/blog",
                    f"https://{domain}/stories",
                ]

                for url in news_urls:
                    try:
                        await page.goto(url, wait_until="domcontentloaded")
                        await page.wait_for_timeout(2000)

                        # Check for article links
                        article_links = await page.locator(
                            'a[href*="/news/"], a[href*="/article/"], a[href*="/story/"]'
                        ).count()
                        if article_links > 5:
                            patterns["article_list_url"] = url
                            patterns["article_list_selector"] = (
                                'a[href*="/news/"], a[href*="/article/"], a[href*="/story/"]'
                            )
                            logger.info(f"🔍 Found article list at: {url}")
                            break
                    except:
                        continue
            except:
                pass

            return patterns

        except Exception as e:
            logger.error(f"❌ Error detecting article patterns: {str(e)}")
            return {}

    async def _analyze_content_structure(
        self, page, soup: BeautifulSoup
    ) -> Dict[str, Any]:
        """
        Analyze content structure and layout.

        Args:
            page: Playwright page object
            soup: BeautifulSoup object

        Returns:
            Content structure dictionary
        """
        try:
            structure = {
                "layout_type": "unknown",
                "main_content_area": "",
                "sidebar_present": False,
                "header_structure": {},
                "footer_structure": {},
                "article_structure": {},
            }

            # Detect layout type
            if soup.find("main") or soup.find(
                class_=lambda x: x and "main" in x.lower()
            ):
                structure["layout_type"] = "semantic"
                structure["main_content_area"] = "main"
            elif soup.find(id="content") or soup.find(class_="content"):
                structure["layout_type"] = "content_area"
                structure["main_content_area"] = "#content, .content"
            elif soup.find(class_=lambda x: x and "container" in x.lower()):
                structure["layout_type"] = "container"
                structure["main_content_area"] = ".container"

            # Check for sidebar
            sidebar_indicators = ["sidebar", "aside", "secondary"]
            for indicator in sidebar_indicators:
                if soup.find(class_=lambda x: x and indicator in x.lower()):
                    structure["sidebar_present"] = True
                    break

            # Analyze header structure
            header = soup.find("header")
            if header:
                structure["header_structure"] = {
                    "has_header": True,
                    "nav_in_header": bool(header.find("nav")),
                    "logo_present": bool(
                        header.find(class_=lambda x: x and "logo" in x.lower())
                    ),
                }

            # Analyze article structure
            articles = soup.find_all("article")
            if articles:
                article = articles[0]  # Analyze first article
                structure["article_structure"] = {
                    "has_article_tag": True,
                    "has_header": bool(article.find("header")),
                    "has_footer": bool(article.find("footer")),
                    "has_time_tag": bool(article.find("time")),
                    "paragraph_count": len(article.find_all("p")),
                }

            return structure

        except Exception as e:
            logger.error(f"❌ Error analyzing content structure: {str(e)}")
            return {}

    def _calculate_complexity_score(self, soup: BeautifulSoup) -> float:
        """
        Calculate complexity score for the website.

        Args:
            soup: BeautifulSoup object

        Returns:
            Complexity score between 0.0 and 1.0
        """
        try:
            complexity_factors = {
                "javascript_elements": 0,
                "dynamic_content": 0,
                "nested_depth": 0,
                "total_elements": 0,
                "interactive_elements": 0,
            }

            # Count JavaScript elements
            js_elements = soup.find_all("script")
            complexity_factors["javascript_elements"] = len(js_elements)

            # Count dynamic content indicators
            dynamic_indicators = soup.find_all(
                class_=lambda x: x
                and any(
                    keyword in x.lower()
                    for keyword in ["dynamic", "ajax", "load", "infinite"]
                )
            )
            complexity_factors["dynamic_content"] = len(dynamic_indicators)

            # Calculate nesting depth
            max_depth = 0
            for element in soup.find_all():
                depth = len(list(element.parents))
                max_depth = max(max_depth, depth)
            complexity_factors["nested_depth"] = max_depth

            # Count total elements
            complexity_factors["total_elements"] = len(soup.find_all())

            # Count interactive elements
            interactive_elements = soup.find_all(
                ["button", "input", "select", "textarea"]
            )
            interactive_elements.extend(
                soup.find_all(
                    class_=lambda x: x
                    and any(
                        keyword in x.lower()
                        for keyword in ["button", "click", "interactive"]
                    )
                )
            )
            complexity_factors["interactive_elements"] = len(interactive_elements)

            # Calculate weighted complexity score
            score = (
                min(complexity_factors["javascript_elements"] / 20, 1.0) * 0.3
                + min(complexity_factors["dynamic_content"] / 10, 1.0) * 0.2
                + min(complexity_factors["nested_depth"] / 50, 1.0) * 0.2
                + min(complexity_factors["total_elements"] / 1000, 1.0) * 0.1
                + min(complexity_factors["interactive_elements"] / 30, 1.0) * 0.2
            )

            return round(score, 2)

        except Exception as e:
            logger.error(f"❌ Error calculating complexity score: {str(e)}")
            return 0.5

    async def _detect_selectors(
        self, page, soup: BeautifulSoup
    ) -> Dict[str, List[str]]:
        """
        Detect useful selectors for scraping.

        Args:
            page: Playwright page object
            soup: BeautifulSoup object

        Returns:
            Dictionary of selector categories and their selectors
        """
        try:
            selectors = {
                "article_links": [],
                "title_selectors": [],
                "content_selectors": [],
                "date_selectors": [],
                "author_selectors": [],
            }

            # Find article links
            link_patterns = [
                'a[href*="/news/"]',
                'a[href*="/article/"]',
                'a[href*="/story/"]',
                'a[href*="/post/"]',
                ".article-title a",
                ".post-title a",
                ".news-title a",
            ]

            for pattern in link_patterns:
                if await page.locator(pattern).count() > 0:
                    selectors["article_links"].append(pattern)

            # Find title selectors
            title_patterns = [
                "h1.title",
                "h1.article-title",
                "h1.post-title",
                "h2.title",
                "h2.article-title",
                ".headline",
                ".article-headline",
            ]

            for pattern in title_patterns:
                if await page.locator(pattern).count() > 0:
                    selectors["title_selectors"].append(pattern)

            # Find content selectors
            content_patterns = [
                ".article-content",
                ".post-content",
                ".entry-content",
                ".content-body",
                ".article-body",
                ".story-content",
            ]

            for pattern in content_patterns:
                if await page.locator(pattern).count() > 0:
                    selectors["content_selectors"].append(pattern)

            # Find date selectors
            date_patterns = [
                "time",
                ".date",
                ".publish-date",
                ".article-date",
                ".post-date",
                ".entry-date",
            ]

            for pattern in date_patterns:
                if await page.locator(pattern).count() > 0:
                    selectors["date_selectors"].append(pattern)

            # Find author selectors
            author_patterns = [
                ".author",
                ".byline",
                ".article-author",
                ".post-author",
                ".writer",
            ]

            for pattern in author_patterns:
                if await page.locator(pattern).count() > 0:
                    selectors["author_selectors"].append(pattern)

            return selectors

        except Exception as e:
            logger.error(f"❌ Error detecting selectors: {str(e)}")
            return {}

    async def _detect_javascript_dependency(self, page) -> bool:
        """
        Detect if the site heavily depends on JavaScript.

        Args:
            page: Playwright page object

        Returns:
            True if JavaScript is required, False otherwise
        """
        try:
            # Check for common JavaScript frameworks
            js_frameworks = [
                'script[src*="react"]',
                'script[src*="angular"]',
                'script[src*="vue"]',
                'script[src*="jquery"]',
                'script[src*="backbone"]',
                'script[src*="ember"]',
            ]

            framework_count = 0
            for framework in js_frameworks:
                if await page.locator(framework).count() > 0:
                    framework_count += 1

            # Check for dynamic content loading
            dynamic_indicators = [
                ".loading",
                ".spinner",
                "[data-ajax]",
                "[data-load]",
                ".infinite-scroll",
            ]

            dynamic_count = 0
            for indicator in dynamic_indicators:
                if await page.locator(indicator).count() > 0:
                    dynamic_count += 1

            # Check for SPA indicators
            spa_indicators = [
                'div[id="root"]',
                'div[id="app"]',
                'div[class*="app"]',
                'div[class*="container"]',
            ]

            spa_count = 0
            for indicator in spa_indicators:
                if await page.locator(indicator).count() > 0:
                    spa_count += 1

            # Determine if JavaScript is required
            js_required = framework_count > 0 or dynamic_count > 2 or spa_count > 1

            logger.info(f"🔍 JavaScript dependency: {js_required}")
            logger.info(
                f"Frameworks: {framework_count}, Dynamic: {dynamic_count}, SPA: {spa_count}"
            )

            return js_required

        except Exception as e:
            logger.error(f"❌ Error detecting JavaScript dependency: {str(e)}")
            return True  # Default to requiring JavaScript for safety

    def clear_cache(self):
        """Clear analysis cache."""
        self.analysis_cache.clear()
        logger.info("🧹 Site structure analysis cache cleared")
