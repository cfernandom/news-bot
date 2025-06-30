"""
Compliance module for ethical web scraping.
Handles robots.txt, rate limiting, and legal requirements.
"""

from .robots_checker import robots_checker, check_robots_compliance, check_multiple_urls_compliance
from .rate_limiter import RateLimiter, get_rate_limiter

__all__ = [
    'robots_checker',
    'check_robots_compliance', 
    'check_multiple_urls_compliance',
    'RateLimiter',
    'get_rate_limiter'
]