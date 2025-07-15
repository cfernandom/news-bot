"""
Configurable rate limiting system for PreventIA News Analytics
Implements domain-specific rate limiting with burst support and compliance monitoring
"""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional

from services.shared.logging.structured_logger import get_logger

logger = get_logger("scraper.rate_limiter")


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting per domain"""

    domain: str
    requests_per_minute: int = 30
    delay_between_requests: float = 2.0
    burst_limit: int = 5
    timeout_seconds: int = 30
    max_concurrent_requests: int = 3
    backoff_factor: float = 1.5  # Exponential backoff multiplier
    max_backoff_seconds: float = 60.0


@dataclass
class RateLimitState:
    """State tracking for rate limiting"""

    last_request_time: float = field(default_factory=time.time)
    request_times: deque = field(default_factory=lambda: deque(maxlen=100))
    current_delay: float = 0.0
    consecutive_failures: int = 0
    is_backing_off: bool = False
    backoff_until: float = 0.0
    total_requests: int = 0
    failed_requests: int = 0


class RateLimiter:
    """
    Intelligent rate limiter with domain-specific configurations
    """

    def __init__(self):
        self.configs: Dict[str, RateLimitConfig] = {}
        self.states: Dict[str, RateLimitState] = defaultdict(RateLimitState)
        self.active_requests: Dict[str, int] = defaultdict(int)
        self._initialize_default_configs()

    def _initialize_default_configs(self):
        """Initialize default rate limiting configurations for known domains"""

        # Medical/Scientific sources - more conservative
        self.configs["medicalxpress.com"] = RateLimitConfig(
            domain="medicalxpress.com",
            requests_per_minute=20,
            delay_between_requests=3.0,
            burst_limit=3,
            timeout_seconds=45,
            max_concurrent_requests=2,
        )

        self.configs["nature.com"] = RateLimitConfig(
            domain="nature.com",
            requests_per_minute=15,
            delay_between_requests=4.0,
            burst_limit=2,
            timeout_seconds=60,
            max_concurrent_requests=1,
        )

        # News sources - moderate
        self.configs["news-medical.net"] = RateLimitConfig(
            domain="news-medical.net",
            requests_per_minute=40,
            delay_between_requests=1.5,
            burst_limit=8,
            timeout_seconds=30,
            max_concurrent_requests=3,
        )

        self.configs["sciencedaily.com"] = RateLimitConfig(
            domain="sciencedaily.com",
            requests_per_minute=30,
            delay_between_requests=2.0,
            burst_limit=5,
            timeout_seconds=30,
            max_concurrent_requests=2,
        )

        # General health sources - standard
        self.configs["breastcancer.org"] = RateLimitConfig(
            domain="breastcancer.org",
            requests_per_minute=50,
            delay_between_requests=1.2,
            burst_limit=10,
            timeout_seconds=25,
            max_concurrent_requests=4,
        )

        self.configs["webmd.com"] = RateLimitConfig(
            domain="webmd.com",
            requests_per_minute=60,
            delay_between_requests=1.0,
            burst_limit=12,
            timeout_seconds=20,
            max_concurrent_requests=5,
        )

        # Default configuration for unknown domains
        self.configs["default"] = RateLimitConfig(
            domain="default",
            requests_per_minute=30,
            delay_between_requests=2.0,
            burst_limit=5,
            timeout_seconds=30,
            max_concurrent_requests=3,
        )

    def get_config(self, domain: str) -> RateLimitConfig:
        """Get rate limit configuration for a domain"""
        return self.configs.get(domain, self.configs["default"])

    def get_state(self, domain: str) -> RateLimitState:
        """Get rate limit state for a domain"""
        return self.states[domain]

    async def acquire(self, domain: str, operation: str = "request") -> bool:
        """
        Acquire permission to make a request to a domain

        Args:
            domain: Target domain
            operation: Operation type for logging

        Returns:
            True if request is allowed, False if rate limited
        """
        config = self.get_config(domain)
        state = self.get_state(domain)
        current_time = time.time()

        # Check if we're in backoff period
        if state.is_backing_off and current_time < state.backoff_until:
            remaining_backoff = state.backoff_until - current_time
            logger.warning(
                "Request blocked due to backoff",
                domain=domain,
                operation=operation,
                remaining_backoff=remaining_backoff,
            )
            return False

        # Reset backoff if period expired
        if state.is_backing_off and current_time >= state.backoff_until:
            state.is_backing_off = False
            state.consecutive_failures = 0
            logger.info("Backoff period expired", domain=domain)

        # Check concurrent request limit
        if self.active_requests[domain] >= config.max_concurrent_requests:
            logger.warning(
                "Request blocked due to concurrent limit",
                domain=domain,
                active_requests=self.active_requests[domain],
                max_concurrent=config.max_concurrent_requests,
            )
            return False

        # Check rate limit (requests per minute)
        state.request_times.append(current_time)
        minute_ago = current_time - 60
        recent_requests = sum(1 for t in state.request_times if t > minute_ago)

        if recent_requests > config.requests_per_minute:
            logger.warning(
                "Request blocked due to rate limit",
                domain=domain,
                recent_requests=recent_requests,
                limit=config.requests_per_minute,
            )
            return False

        # Check minimum delay between requests
        time_since_last = current_time - state.last_request_time
        required_delay = config.delay_between_requests + state.current_delay

        if time_since_last < required_delay:
            sleep_time = required_delay - time_since_last
            logger.debug(
                "Applying request delay",
                domain=domain,
                sleep_time=sleep_time,
                required_delay=required_delay,
            )
            await asyncio.sleep(sleep_time)

        # Update state
        state.last_request_time = time.time()
        state.total_requests += 1
        self.active_requests[domain] += 1

        logger.debug(
            "Request approved",
            domain=domain,
            operation=operation,
            total_requests=state.total_requests,
            active_requests=self.active_requests[domain],
        )

        return True

    def release(self, domain: str, success: bool = True, operation: str = "request"):
        """
        Release a request slot and update state

        Args:
            domain: Target domain
            success: Whether the request was successful
            operation: Operation type for logging
        """
        state = self.get_state(domain)
        config = self.get_config(domain)

        # Update active requests
        self.active_requests[domain] = max(0, self.active_requests[domain] - 1)

        if success:
            # Reset failure tracking on success
            state.consecutive_failures = 0
            state.current_delay = 0.0

            logger.debug(
                "Request completed successfully",
                domain=domain,
                operation=operation,
                active_requests=self.active_requests[domain],
            )
        else:
            # Handle failure
            state.failed_requests += 1
            state.consecutive_failures += 1

            # Apply exponential backoff
            if state.consecutive_failures >= 3:
                backoff_duration = min(
                    config.delay_between_requests
                    * (config.backoff_factor**state.consecutive_failures),
                    config.max_backoff_seconds,
                )

                state.is_backing_off = True
                state.backoff_until = time.time() + backoff_duration

                logger.warning(
                    "Applying exponential backoff",
                    domain=domain,
                    consecutive_failures=state.consecutive_failures,
                    backoff_duration=backoff_duration,
                )
            else:
                # Increase delay for next request
                state.current_delay = min(
                    state.current_delay + config.delay_between_requests * 0.5,
                    config.max_backoff_seconds,
                )

            logger.warning(
                "Request failed",
                domain=domain,
                operation=operation,
                consecutive_failures=state.consecutive_failures,
                failed_requests=state.failed_requests,
            )

    def get_stats(self, domain: str) -> Dict:
        """Get rate limiting statistics for a domain"""
        state = self.get_state(domain)
        config = self.get_config(domain)
        current_time = time.time()

        # Calculate recent request rate
        minute_ago = current_time - 60
        recent_requests = sum(1 for t in state.request_times if t > minute_ago)

        return {
            "domain": domain,
            "total_requests": state.total_requests,
            "failed_requests": state.failed_requests,
            "success_rate": (state.total_requests - state.failed_requests)
            / max(1, state.total_requests),
            "recent_requests_per_minute": recent_requests,
            "rate_limit": config.requests_per_minute,
            "active_requests": self.active_requests[domain],
            "max_concurrent": config.max_concurrent_requests,
            "is_backing_off": state.is_backing_off,
            "consecutive_failures": state.consecutive_failures,
            "current_delay": state.current_delay,
            "backoff_remaining": (
                max(0, state.backoff_until - current_time)
                if state.is_backing_off
                else 0
            ),
        }

    def get_all_stats(self) -> Dict[str, Dict]:
        """Get rate limiting statistics for all domains"""
        return {domain: self.get_stats(domain) for domain in self.states.keys()}

    def update_config(self, domain: str, **kwargs):
        """Update rate limiting configuration for a domain"""
        if domain in self.configs:
            config = self.configs[domain]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
                    logger.info(
                        f"Updated {key} for {domain}",
                        domain=domain,
                        key=key,
                        value=value,
                    )
        else:
            logger.warning(
                f"Domain {domain} not found in configurations", domain=domain
            )


# Global rate limiter instance
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance"""
    return _rate_limiter


# Context manager for easy rate limiting
class RateLimitedRequest:
    """Context manager for rate-limited requests"""

    def __init__(self, domain: str, operation: str = "request"):
        self.domain = domain
        self.operation = operation
        self.rate_limiter = get_rate_limiter()
        self.acquired = False

    async def __aenter__(self):
        self.acquired = await self.rate_limiter.acquire(self.domain, self.operation)
        if not self.acquired:
            raise Exception(f"Rate limit exceeded for {self.domain}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.acquired:
            success = exc_type is None
            self.rate_limiter.release(self.domain, success, self.operation)


# Example usage
async def example_usage():
    """Example of how to use the rate limiter"""
    rate_limiter = get_rate_limiter()

    # Method 1: Manual acquire/release
    if await rate_limiter.acquire("medicalxpress.com", "scrape_articles"):
        try:
            # Make your request here
            print("Making request...")
            await asyncio.sleep(1)  # Simulate request
            rate_limiter.release("medicalxpress.com", True, "scrape_articles")
        except Exception as e:
            rate_limiter.release("medicalxpress.com", False, "scrape_articles")
            raise

    # Method 2: Context manager (recommended)
    try:
        async with RateLimitedRequest("medicalxpress.com", "scrape_articles"):
            # Make your request here
            print("Making request with context manager...")
            await asyncio.sleep(1)  # Simulate request
    except Exception as e:
        print(f"Request failed: {e}")

    # Get statistics
    stats = rate_limiter.get_stats("medicalxpress.com")
    print(f"Rate limiter stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
