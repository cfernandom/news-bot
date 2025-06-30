"""
Rate limiting and respectful crawling delays for ethical web scraping.
Prevents overwhelming target servers and respects crawl-delay directives.
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Dict, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Implements respectful rate limiting for web scraping operations.
    Supports per-domain rate limiting and crawl-delay compliance.
    """

    def __init__(
        self,
        default_delay: float = 2.0,
        min_delay: float = 1.0,
        max_delay: float = 10.0,
    ):
        """
        Initialize rate limiter.

        Args:
            default_delay: Default delay between requests (seconds)
            min_delay: Minimum delay allowed (seconds)
            max_delay: Maximum delay allowed (seconds)
        """
        self.default_delay = default_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

        # Track last request time per domain
        self._last_request_time: Dict[str, float] = defaultdict(float)

        # Domain-specific delays (from robots.txt or manual override)
        self._domain_delays: Dict[str, float] = {}

        # Request counters for logging
        self._request_counts: Dict[str, int] = defaultdict(int)

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc

    def set_domain_delay(self, domain: str, delay: float):
        """
        Set custom delay for specific domain.

        Args:
            domain: Domain name (e.g., 'www.webmd.com')
            delay: Delay in seconds
        """
        # Enforce min/max limits
        delay = max(self.min_delay, min(delay, self.max_delay))
        self._domain_delays[domain] = delay
        logger.info(f"Set custom delay for {domain}: {delay}s")

    def get_delay_for_domain(self, domain: str) -> float:
        """
        Get the delay that should be used for a domain.

        Args:
            domain: Domain name

        Returns:
            Delay in seconds
        """
        return self._domain_delays.get(domain, self.default_delay)

    async def wait_if_needed(self, url: str) -> float:
        """
        Wait if needed to respect rate limits for the domain.

        Args:
            url: URL being accessed

        Returns:
            Actual delay applied (seconds)
        """
        domain = self._get_domain(url)
        current_time = time.time()
        last_request = self._last_request_time[domain]
        required_delay = self.get_delay_for_domain(domain)

        # Calculate time since last request
        time_since_last = current_time - last_request

        if time_since_last < required_delay:
            # Need to wait
            wait_time = required_delay - time_since_last
            logger.info(f"Rate limiting {domain}: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
            actual_delay = wait_time
        else:
            # No wait needed
            actual_delay = 0.0

        # Update last request time
        self._last_request_time[domain] = time.time()
        self._request_counts[domain] += 1

        if self._request_counts[domain] % 10 == 0:
            logger.info(
                f"Domain {domain}: {self._request_counts[domain]} requests processed"
            )

        return actual_delay

    def get_stats(self) -> Dict[str, Dict]:
        """
        Get rate limiting statistics.

        Returns:
            Dictionary with stats per domain
        """
        stats = {}
        for domain in set(
            list(self._last_request_time.keys()) + list(self._request_counts.keys())
        ):
            stats[domain] = {
                "request_count": self._request_counts[domain],
                "configured_delay": self.get_delay_for_domain(domain),
                "last_request_time": self._last_request_time[domain],
            }
        return stats

    def reset_domain_stats(self, domain: str):
        """Reset statistics for a specific domain."""
        if domain in self._last_request_time:
            del self._last_request_time[domain]
        if domain in self._request_counts:
            del self._request_counts[domain]
        logger.info(f"Reset stats for domain: {domain}")

    def reset_all_stats(self):
        """Reset all statistics."""
        self._last_request_time.clear()
        self._request_counts.clear()
        logger.info("Reset all rate limiting stats")


# Global rate limiter instance
_global_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _global_rate_limiter


async def apply_rate_limit(url: str) -> float:
    """
    Convenience function to apply rate limiting to a URL.

    Args:
        url: URL being accessed

    Returns:
        Actual delay applied (seconds)
    """
    return await _global_rate_limiter.wait_if_needed(url)


def configure_domain_delay(domain: str, delay: float):
    """
    Convenience function to configure delay for a domain.

    Args:
        domain: Domain name
        delay: Delay in seconds
    """
    _global_rate_limiter.set_domain_delay(domain, delay)
