"""
Intelligent caching system for PreventIA News Analytics
Prevents re-scraping of already processed content and optimizes performance
"""

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import redis

from services.shared.logging.structured_logger import get_logger

logger = get_logger("scraper.cache_manager")


class CacheType(Enum):
    """Types of cache entries"""

    ARTICLE = "article"
    PAGE_CONTENT = "page_content"
    SCRAPER_RUN = "scraper_run"
    RATE_LIMIT = "rate_limit"


@dataclass
class CacheEntry:
    """Cache entry with metadata"""

    key: str
    value: Any
    cache_type: CacheType
    domain: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    content_hash: Optional[str] = None


class CacheManager:
    """
    Intelligent cache manager with Redis backend
    Handles article deduplication, page content caching, and performance optimization
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", db: int = 1):
        try:
            self.redis_client = redis.from_url(redis_url, db=db, decode_responses=True)
            self.redis_client.ping()
            logger.info("Connected to Redis cache", redis_url=redis_url, db=db)
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            self.redis_client = None

        self.cache_configs = self._initialize_cache_configs()
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0}

    def _initialize_cache_configs(self) -> Dict[CacheType, Dict]:
        """Initialize cache configurations for different types"""
        return {
            CacheType.ARTICLE: {
                "ttl_hours": 24 * 7,  # 1 week
                "max_entries": 10000,
                "cleanup_threshold": 0.8,
            },
            CacheType.PAGE_CONTENT: {
                "ttl_hours": 6,  # 6 hours
                "max_entries": 1000,
                "cleanup_threshold": 0.9,
            },
            CacheType.SCRAPER_RUN: {
                "ttl_hours": 24,  # 1 day
                "max_entries": 100,
                "cleanup_threshold": 0.7,
            },
            CacheType.RATE_LIMIT: {
                "ttl_hours": 1,  # 1 hour
                "max_entries": 1000,
                "cleanup_threshold": 0.9,
            },
        }

    def _generate_key(
        self, cache_type: CacheType, identifier: str, domain: str = ""
    ) -> str:
        """Generate a cache key"""
        return f"preventia:{cache_type.value}:{domain}:{identifier}"

    def _generate_content_hash(self, content: str) -> str:
        """Generate content hash for deduplication"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _serialize_entry(self, entry: CacheEntry) -> str:
        """Serialize cache entry to JSON"""
        data = asdict(entry)
        # Convert datetime objects to ISO strings
        for key in ["created_at", "expires_at", "last_accessed"]:
            if data[key]:
                data[key] = data[key].isoformat()
        # Convert enum to string
        data["cache_type"] = data["cache_type"].value
        return json.dumps(data)

    def _deserialize_entry(self, data: str) -> CacheEntry:
        """Deserialize cache entry from JSON"""
        parsed = json.loads(data)
        # Convert ISO strings to datetime objects
        for key in ["created_at", "expires_at", "last_accessed"]:
            if parsed[key]:
                parsed[key] = datetime.fromisoformat(parsed[key])
        # Convert string to enum
        parsed["cache_type"] = CacheType(parsed["cache_type"])
        return CacheEntry(**parsed)

    def is_available(self) -> bool:
        """Check if cache is available"""
        return self.redis_client is not None

    def get_article_cache_key(self, url: str, domain: str) -> str:
        """Get cache key for an article"""
        url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
        return self._generate_key(CacheType.ARTICLE, url_hash, domain)

    def is_article_cached(self, url: str, domain: str) -> bool:
        """Check if an article is already cached"""
        if not self.is_available():
            return False

        key = self.get_article_cache_key(url, domain)
        exists = self.redis_client.exists(key)

        if exists:
            self.stats["hits"] += 1
            logger.debug("Article cache hit", url=url, domain=domain)
        else:
            self.stats["misses"] += 1
            logger.debug("Article cache miss", url=url, domain=domain)

        return bool(exists)

    def cache_article(
        self, url: str, domain: str, content: str, metadata: Optional[Dict] = None
    ) -> bool:
        """Cache an article"""
        if not self.is_available():
            return False

        try:
            key = self.get_article_cache_key(url, domain)
            config = self.cache_configs[CacheType.ARTICLE]

            entry = CacheEntry(
                key=key,
                value={"url": url, "content": content, "metadata": metadata or {}},
                cache_type=CacheType.ARTICLE,
                domain=domain,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=config["ttl_hours"]),
                content_hash=self._generate_content_hash(content),
            )

            serialized = self._serialize_entry(entry)
            self.redis_client.setex(key, int(config["ttl_hours"] * 3600), serialized)

            self.stats["sets"] += 1
            logger.debug(
                "Article cached", url=url, domain=domain, content_length=len(content)
            )
            return True

        except Exception as e:
            logger.error(
                "Failed to cache article", url=url, domain=domain, error=str(e)
            )
            return False

    def get_cached_article(self, url: str, domain: str) -> Optional[Dict]:
        """Get cached article"""
        if not self.is_available():
            return None

        try:
            key = self.get_article_cache_key(url, domain)
            data = self.redis_client.get(key)

            if data:
                entry = self._deserialize_entry(data)

                # Update access statistics
                entry.access_count += 1
                entry.last_accessed = datetime.now()

                # Update cache entry
                self.redis_client.setex(
                    key,
                    int(self.cache_configs[CacheType.ARTICLE]["ttl_hours"] * 3600),
                    self._serialize_entry(entry),
                )

                self.stats["hits"] += 1
                logger.debug("Article cache hit", url=url, domain=domain)
                return entry.value

            self.stats["misses"] += 1
            return None

        except Exception as e:
            logger.error(
                "Failed to get cached article", url=url, domain=domain, error=str(e)
            )
            return None

    def cache_page_content(self, url: str, domain: str, html_content: str) -> bool:
        """Cache page HTML content"""
        if not self.is_available():
            return False

        try:
            url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
            key = self._generate_key(CacheType.PAGE_CONTENT, url_hash, domain)
            config = self.cache_configs[CacheType.PAGE_CONTENT]

            entry = CacheEntry(
                key=key,
                value={
                    "url": url,
                    "html_content": html_content,
                    "content_length": len(html_content),
                },
                cache_type=CacheType.PAGE_CONTENT,
                domain=domain,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=config["ttl_hours"]),
                content_hash=self._generate_content_hash(html_content),
            )

            self.redis_client.setex(
                key, int(config["ttl_hours"] * 3600), self._serialize_entry(entry)
            )

            self.stats["sets"] += 1
            logger.debug(
                "Page content cached",
                url=url,
                domain=domain,
                content_length=len(html_content),
            )
            return True

        except Exception as e:
            logger.error(
                "Failed to cache page content", url=url, domain=domain, error=str(e)
            )
            return False

    def get_cached_page_content(self, url: str, domain: str) -> Optional[str]:
        """Get cached page content"""
        if not self.is_available():
            return None

        try:
            url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
            key = self._generate_key(CacheType.PAGE_CONTENT, url_hash, domain)
            data = self.redis_client.get(key)

            if data:
                entry = self._deserialize_entry(data)
                self.stats["hits"] += 1
                logger.debug("Page content cache hit", url=url, domain=domain)
                return entry.value["html_content"]

            self.stats["misses"] += 1
            return None

        except Exception as e:
            logger.error(
                "Failed to get cached page content",
                url=url,
                domain=domain,
                error=str(e),
            )
            return None

    def cache_scraper_run(
        self,
        domain: str,
        scraper_name: str,
        articles_count: int,
        execution_time: float,
        success: bool,
    ) -> bool:
        """Cache scraper run results"""
        if not self.is_available():
            return False

        try:
            run_id = f"{scraper_name}_{int(time.time())}"
            key = self._generate_key(CacheType.SCRAPER_RUN, run_id, domain)
            config = self.cache_configs[CacheType.SCRAPER_RUN]

            entry = CacheEntry(
                key=key,
                value={
                    "domain": domain,
                    "scraper_name": scraper_name,
                    "articles_count": articles_count,
                    "execution_time": execution_time,
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                },
                cache_type=CacheType.SCRAPER_RUN,
                domain=domain,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=config["ttl_hours"]),
            )

            self.redis_client.setex(
                key, int(config["ttl_hours"] * 3600), self._serialize_entry(entry)
            )

            self.stats["sets"] += 1
            logger.debug("Scraper run cached", domain=domain, scraper_name=scraper_name)
            return True

        except Exception as e:
            logger.error(
                "Failed to cache scraper run",
                domain=domain,
                scraper_name=scraper_name,
                error=str(e),
            )
            return False

    def get_recent_scraper_runs(self, domain: str, hours: int = 24) -> List[Dict]:
        """Get recent scraper runs for a domain"""
        if not self.is_available():
            return []

        try:
            pattern = self._generate_key(CacheType.SCRAPER_RUN, "*", domain)
            keys = self.redis_client.keys(pattern)

            runs = []
            for key in keys:
                data = self.redis_client.get(key)
                if data:
                    entry = self._deserialize_entry(data)
                    # Check if within time window
                    if entry.created_at > datetime.now() - timedelta(hours=hours):
                        runs.append(entry.value)

            # Sort by timestamp
            runs.sort(key=lambda x: x["timestamp"], reverse=True)
            return runs

        except Exception as e:
            logger.error(
                "Failed to get recent scraper runs", domain=domain, error=str(e)
            )
            return []

    def cleanup_expired_entries(self, cache_type: Optional[CacheType] = None) -> int:
        """Clean up expired cache entries"""
        if not self.is_available():
            return 0

        cleaned = 0
        try:
            cache_types = [cache_type] if cache_type else list(CacheType)

            for ct in cache_types:
                pattern = self._generate_key(ct, "*", "*")
                keys = self.redis_client.keys(pattern)

                for key in keys:
                    data = self.redis_client.get(key)
                    if data:
                        try:
                            entry = self._deserialize_entry(data)
                            if entry.expires_at and entry.expires_at < datetime.now():
                                self.redis_client.delete(key)
                                cleaned += 1
                        except:
                            # If we can't deserialize, delete the entry
                            self.redis_client.delete(key)
                            cleaned += 1

            if cleaned > 0:
                logger.info("Cleaned up expired cache entries", cleaned_count=cleaned)

            return cleaned

        except Exception as e:
            logger.error("Failed to cleanup expired entries", error=str(e))
            return 0

    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        stats = self.stats.copy()

        if self.is_available():
            try:
                # Get Redis info
                info = self.redis_client.info()
                stats.update(
                    {
                        "redis_memory_used": info.get("used_memory_human", "N/A"),
                        "redis_keys": (
                            info.get("db1", {}).get("keys", 0) if "db1" in info else 0
                        ),
                        "redis_connected": True,
                    }
                )

                # Calculate hit rate
                total_requests = stats["hits"] + stats["misses"]
                stats["hit_rate"] = (
                    stats["hits"] / total_requests if total_requests > 0 else 0
                )

                # Get cache type breakdown
                cache_breakdown = {}
                for cache_type in CacheType:
                    pattern = self._generate_key(cache_type, "*", "*")
                    keys = self.redis_client.keys(pattern)
                    cache_breakdown[cache_type.value] = len(keys)

                stats["cache_breakdown"] = cache_breakdown

            except Exception as e:
                logger.error("Failed to get cache stats", error=str(e))
                stats["redis_connected"] = False
        else:
            stats["redis_connected"] = False

        return stats

    def clear_cache(
        self, cache_type: Optional[CacheType] = None, domain: Optional[str] = None
    ) -> int:
        """Clear cache entries"""
        if not self.is_available():
            return 0

        try:
            if cache_type and domain:
                pattern = self._generate_key(cache_type, "*", domain)
            elif cache_type:
                pattern = self._generate_key(cache_type, "*", "*")
            elif domain:
                pattern = f"preventia:*:{domain}:*"
            else:
                pattern = "preventia:*"

            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                self.stats["deletes"] += deleted
                logger.info("Cache cleared", pattern=pattern, deleted_count=deleted)
                return deleted

            return 0

        except Exception as e:
            logger.error("Failed to clear cache", error=str(e))
            return 0


# Global cache manager instance
_cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance"""
    return _cache_manager


# Context manager for caching operations
class CachedOperation:
    """Context manager for cached operations"""

    def __init__(
        self, cache_key: str, cache_type: CacheType, domain: str, ttl_hours: int = 24
    ):
        self.cache_key = cache_key
        self.cache_type = cache_type
        self.domain = domain
        self.ttl_hours = ttl_hours
        self.cache_manager = get_cache_manager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_cached(self):
        """Get cached value"""
        return self.cache_manager.get_cached_article(self.cache_key, self.domain)

    def cache_result(self, result):
        """Cache the result"""
        return self.cache_manager.cache_article(self.cache_key, self.domain, result)


if __name__ == "__main__":
    # Example usage
    cache_manager = get_cache_manager()

    # Test article caching
    test_url = "https://example.com/article"
    test_domain = "example.com"
    test_content = "This is test article content"

    print(f"Cache available: {cache_manager.is_available()}")

    # Cache an article
    cache_manager.cache_article(test_url, test_domain, test_content)

    # Check if cached
    print(f"Article cached: {cache_manager.is_article_cached(test_url, test_domain)}")

    # Get cached content
    cached = cache_manager.get_cached_article(test_url, test_domain)
    print(f"Cached content: {cached}")

    # Get stats
    stats = cache_manager.get_cache_stats()
    print(f"Cache stats: {stats}")
