"""
Compliance module for ethical web scraping.
Handles robots.txt, rate limiting, and legal requirements.
"""

from .rate_limiter import RateLimiter, get_rate_limiter
from .robots_checker import (
    check_multiple_urls_compliance,
    check_robots_compliance,
    robots_checker,
)

__all__ = [
    "robots_checker",
    "check_robots_compliance",
    "check_multiple_urls_compliance",
    "RateLimiter",
    "get_rate_limiter",
]
