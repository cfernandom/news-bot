"""
Robots.txt compliance checker for ethical web scraping.
Ensures PreventIA respects website crawling policies.
"""

import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from typing import Optional, Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RobotsChecker:
    """
    Handles robots.txt compliance checking for web scraping operations.
    Implements caching and respectful crawling guidelines.
    """
    
    def __init__(self, user_agent: str = "PreventIA-NewsBot/1.0"):
        self.user_agent = user_agent
        self._cache: Dict[str, tuple] = {}  # domain -> (RobotFileParser, timestamp)
        self._cache_duration = timedelta(hours=24)
    
    def _get_robots_url(self, url: str) -> str:
        """Generate robots.txt URL from any page URL."""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        return urljoin(base_url, '/robots.txt')
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL for caching."""
        return urlparse(url).netloc
    
    async def _fetch_robots_txt(self, robots_url: str) -> Optional[str]:
        """Fetch robots.txt content asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    robots_url,
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={'User-Agent': self.user_agent}
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.warning(f"robots.txt not found for {robots_url} (status: {response.status})")
                        return None
        except Exception as e:
            logger.error(f"Error fetching robots.txt from {robots_url}: {e}")
            return None
    
    def _parse_robots_txt(self, robots_content: str) -> RobotFileParser:
        """Parse robots.txt content using Python 3.13 compatible method."""
        rp = RobotFileParser()
        
        # Use temporary file approach for Python 3.13 compatibility
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write(robots_content)
            tmp.flush()
            
            # Set URL and read from file
            rp.set_url(f"file://{tmp.name}")
            try:
                rp.read()  # This reads from the URL set above
            except Exception as e:
                logger.warning(f"Error parsing robots.txt with standard method: {e}")
                # Fallback to manual parsing
                return self._create_permissive_parser()
        
        # Clean up temp file
        import os
        try:
            os.unlink(tmp.name)
        except:
            pass
            
        return rp
    
    def _create_permissive_parser(self) -> RobotFileParser:
        """Create a permissive robots parser for fallback."""
        rp = RobotFileParser()
        rp.set_url("dummy")
        # Create minimal robots.txt that allows everything
        rp.can_fetch = lambda user_agent, url: True
        rp.crawl_delay = lambda user_agent: None
        return rp
    
    async def can_fetch(self, url: str) -> bool:
        """
        Check if URL can be fetched according to robots.txt.
        
        Args:
            url: The URL to check
            
        Returns:
            True if allowed, False if disallowed
        """
        domain = self._get_domain(url)
        robots_url = self._get_robots_url(url)
        
        # Check cache first
        if domain in self._cache:
            rp, timestamp = self._cache[domain]
            if datetime.now() - timestamp < self._cache_duration:
                return rp.can_fetch(self.user_agent, url)
        
        # Fetch and parse robots.txt
        robots_content = await self._fetch_robots_txt(robots_url)
        
        if robots_content is None:
            # If no robots.txt found, assume allowed (common practice)
            logger.info(f"No robots.txt found for {domain}, assuming allowed")
            return True
        
        try:
            rp = self._parse_robots_txt(robots_content)
            self._cache[domain] = (rp, datetime.now())
            
            allowed = rp.can_fetch(self.user_agent, url)
            logger.info(f"robots.txt check for {url}: {'ALLOWED' if allowed else 'DISALLOWED'}")
            return allowed
            
        except Exception as e:
            logger.error(f"Error parsing robots.txt for {domain}: {e}")
            # On error, assume allowed to prevent blocking legitimate scraping
            return True
    
    def get_crawl_delay(self, url: str) -> Optional[float]:
        """
        Get crawl delay from robots.txt if specified.
        
        Args:
            url: The URL to check
            
        Returns:
            Delay in seconds, or None if not specified
        """
        domain = self._get_domain(url)
        
        if domain in self._cache:
            rp, timestamp = self._cache[domain]
            if datetime.now() - timestamp < self._cache_duration:
                return rp.crawl_delay(self.user_agent)
        
        return None
    
    async def check_multiple_urls(self, urls: List[str]) -> Dict[str, bool]:
        """
        Check multiple URLs for robots.txt compliance.
        
        Args:
            urls: List of URLs to check
            
        Returns:
            Dictionary mapping URLs to their allowed status
        """
        results = {}
        
        # Group URLs by domain to minimize robots.txt fetches
        domains_to_urls = {}
        for url in urls:
            domain = self._get_domain(url)
            if domain not in domains_to_urls:
                domains_to_urls[domain] = []
            domains_to_urls[domain].append(url)
        
        # Check each domain's robots.txt once
        for domain, domain_urls in domains_to_urls.items():
            # Use first URL from domain to fetch robots.txt
            sample_url = domain_urls[0]
            
            # Check all URLs from this domain
            for url in domain_urls:
                allowed = await self.can_fetch(url)
                results[url] = allowed
        
        return results
    
    def clear_cache(self):
        """Clear the robots.txt cache."""
        self._cache.clear()
        logger.info("Robots.txt cache cleared")

# Global instance for use across scrapers
robots_checker = RobotsChecker()

async def check_robots_compliance(url: str) -> bool:
    """
    Convenience function to check a single URL.
    
    Args:
        url: The URL to check
        
    Returns:
        True if allowed, False if disallowed
    """
    return await robots_checker.can_fetch(url)

async def check_multiple_urls_compliance(urls: List[str]) -> Dict[str, bool]:
    """
    Convenience function to check multiple URLs.
    
    Args:
        urls: List of URLs to check
        
    Returns:
        Dictionary mapping URLs to their allowed status
    """
    return await robots_checker.check_multiple_urls(urls)