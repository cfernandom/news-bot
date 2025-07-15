"""
Configurable scraper settings per source for PreventIA News Analytics
Manages domain-specific configurations for scraping behavior
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional

from services.shared.config import settings
from services.shared.logging.structured_logger import get_logger

logger = get_logger("scraper.config")


@dataclass
class ScraperConfig:
    """Configuration for scraper behavior per source"""

    domain: str
    max_articles_per_run: int = 50
    max_concurrent_requests: int = 3
    timeout_seconds: int = 30
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.0

    # Content filtering
    min_content_length: int = 0  # Allow empty content for metadata-only scrapers
    max_content_length: int = 50000
    min_title_length: int = 10
    max_title_length: int = 200

    # Date handling
    date_required: bool = settings.scraper.require_date
    max_article_age_days: int = 30

    # Performance settings
    enable_caching: bool = settings.scraper.enable_caching
    cache_ttl_hours: int = settings.scraper.cache_ttl_hours
    use_rate_limiting: bool = settings.scraper.enable_rate_limiting

    # Quality filters
    skip_duplicates: bool = True
    require_summary: bool = settings.scraper.require_summary
    min_summary_length: int = settings.scraper.min_summary_length

    # Compliance settings
    respect_robots_txt: bool = True
    custom_user_agent: Optional[str] = None
    custom_headers: Optional[Dict[str, str]] = None

    # Scraping behavior
    follow_pagination: bool = True
    max_pages: int = 5
    extract_full_content: bool = False

    # Error handling
    continue_on_error: bool = True
    max_consecutive_errors: int = 10

    # Monitoring
    enable_metrics: bool = True
    log_level: str = "INFO"


class ScraperConfigManager:
    """
    Manages scraper configurations per domain with fallback to defaults
    """

    def __init__(self):
        self.configs: Dict[str, ScraperConfig] = {}
        self.default_config = ScraperConfig(
            domain="default",
            timeout_seconds=settings.scraper.default_timeout,
            retry_attempts=settings.scraper.default_retry_attempts,
            retry_delay_seconds=settings.scraper.default_retry_delay,
            min_content_length=settings.scraper.min_content_length,
            min_title_length=settings.scraper.min_title_length,
            custom_user_agent=settings.scraper.default_user_agent,
            respect_robots_txt=settings.scraper.respect_robots_txt,
        )
        self._initialize_domain_configs()

    def _initialize_domain_configs(self):
        """Initialize domain-specific configurations"""

        # Medical/Scientific sources - Conservative approach
        self.configs["medicalxpress.com"] = ScraperConfig(
            domain="medicalxpress.com",
            max_articles_per_run=20,
            max_concurrent_requests=2,
            timeout_seconds=45,
            retry_attempts=2,
            retry_delay_seconds=3.0,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=60,
            cache_ttl_hours=48,
            max_pages=3,
            max_consecutive_errors=5,
            custom_user_agent="PreventIA-Research-Bot/1.0 (Academic Research; UCOMPENSAR)",
        )

        self.configs["nature.com"] = ScraperConfig(
            domain="nature.com",
            max_articles_per_run=15,
            max_concurrent_requests=1,
            timeout_seconds=60,
            retry_attempts=1,
            retry_delay_seconds=5.0,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=90,
            cache_ttl_hours=72,
            max_pages=2,
            max_consecutive_errors=3,
            custom_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            },
        )

        # News sources - Moderate approach
        self.configs["news-medical.net"] = ScraperConfig(
            domain="news-medical.net",
            max_articles_per_run=40,
            max_concurrent_requests=3,
            timeout_seconds=30,
            retry_attempts=3,
            retry_delay_seconds=2.0,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=21,
            cache_ttl_hours=12,
            max_pages=4,
            extract_full_content=True,
        )

        self.configs["sciencedaily.com"] = ScraperConfig(
            domain="sciencedaily.com",
            max_articles_per_run=30,
            max_concurrent_requests=2,
            timeout_seconds=35,
            retry_attempts=2,
            retry_delay_seconds=2.5,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=30,
            cache_ttl_hours=24,
            max_pages=3,
            require_summary=True,
            min_summary_length=20,  # Aligned with business requirements
        )

        # Health information sources - Standard approach
        self.configs["breastcancer.org"] = ScraperConfig(
            domain="breastcancer.org",
            max_articles_per_run=50,
            max_concurrent_requests=4,
            timeout_seconds=25,
            retry_attempts=3,
            retry_delay_seconds=1.5,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=14,
            cache_ttl_hours=6,
            max_pages=5,
            extract_full_content=True,
            require_summary=True,  # Business requirement: resumen es necesario  # Don't require summaries
        )

        self.configs["breastcancernow.org"] = ScraperConfig(
            domain="breastcancernow.org",
            max_articles_per_run=35,
            max_concurrent_requests=3,
            timeout_seconds=30,
            retry_attempts=2,
            retry_delay_seconds=2.0,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=21,
            cache_ttl_hours=12,
            max_pages=3,
            require_summary=True,  # Business requirement: resumen es necesario
        )

        self.configs["webmd.com"] = ScraperConfig(
            domain="webmd.com",
            max_articles_per_run=60,
            max_concurrent_requests=5,
            timeout_seconds=20,
            retry_attempts=3,
            retry_delay_seconds=1.0,
            min_content_length=0,  # Allow metadata-only articles
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=7,
            cache_ttl_hours=4,
            max_pages=6,
            continue_on_error=True,
            max_consecutive_errors=15,
        )

        self.configs["curetoday.com"] = ScraperConfig(
            domain="curetoday.com",
            max_articles_per_run=25,
            max_concurrent_requests=2,
            timeout_seconds=40,
            retry_attempts=2,
            retry_delay_seconds=2.0,
            min_content_length=0,  # Allow metadata-only
            date_required=True,  # Business requirement: fecha es necesaria
            max_article_age_days=30,
            cache_ttl_hours=18,
            max_pages=3,
            extract_full_content=True,
        )

        logger.info(
            "Initialized scraper configurations", total_configs=len(self.configs)
        )

    def get_config(self, domain: str) -> ScraperConfig:
        """Get configuration for a domain"""
        config = self.configs.get(domain, self.default_config)
        logger.debug(
            "Retrieved config", domain=domain, config_found=domain in self.configs
        )
        return config

    def update_config(self, domain: str, **kwargs) -> bool:
        """Update configuration for a domain"""
        try:
            if domain not in self.configs:
                # Create new config based on default
                self.configs[domain] = ScraperConfig(domain=domain)

            config = self.configs[domain]
            updated_fields = []

            for key, value in kwargs.items():
                if hasattr(config, key):
                    old_value = getattr(config, key)
                    setattr(config, key, value)
                    updated_fields.append(f"{key}: {old_value} → {value}")
                else:
                    logger.warning(
                        f"Invalid config field: {key}", domain=domain, field=key
                    )
                    return False

            logger.info(
                "Updated scraper config", domain=domain, updated_fields=updated_fields
            )
            return True

        except Exception as e:
            logger.error("Failed to update config", domain=domain, error=str(e))
            return False

    def get_all_configs(self) -> Dict[str, ScraperConfig]:
        """Get all configurations"""
        return self.configs.copy()

    def validate_config(self, config: ScraperConfig) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []

        # Validate numeric ranges
        if config.max_articles_per_run < 1 or config.max_articles_per_run > 1000:
            issues.append("max_articles_per_run must be between 1 and 1000")

        if config.max_concurrent_requests < 1 or config.max_concurrent_requests > 10:
            issues.append("max_concurrent_requests must be between 1 and 10")

        if config.timeout_seconds < 5 or config.timeout_seconds > 300:
            issues.append("timeout_seconds must be between 5 and 300")

        if config.retry_attempts < 0 or config.retry_attempts > 10:
            issues.append("retry_attempts must be between 0 and 10")

        if config.min_content_length < 0 or config.min_content_length > 1000:
            issues.append("min_content_length must be between 0 and 1000")

        if config.max_content_length < config.min_content_length:
            issues.append("max_content_length must be greater than min_content_length")

        if config.max_article_age_days < 1 or config.max_article_age_days > 365:
            issues.append("max_article_age_days must be between 1 and 365")

        if config.cache_ttl_hours < 1 or config.cache_ttl_hours > 168:  # 1 week
            issues.append("cache_ttl_hours must be between 1 and 168")

        if config.max_pages < 1 or config.max_pages > 20:
            issues.append("max_pages must be between 1 and 20")

        if config.max_consecutive_errors < 1 or config.max_consecutive_errors > 50:
            issues.append("max_consecutive_errors must be between 1 and 50")

        # Validate string fields
        if config.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            issues.append(
                "log_level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )

        return issues

    def export_config(self, domain: str) -> Optional[str]:
        """Export configuration as JSON"""
        try:
            config = self.get_config(domain)
            config_dict = {
                "domain": config.domain,
                "max_articles_per_run": config.max_articles_per_run,
                "max_concurrent_requests": config.max_concurrent_requests,
                "timeout_seconds": config.timeout_seconds,
                "retry_attempts": config.retry_attempts,
                "retry_delay_seconds": config.retry_delay_seconds,
                "min_content_length": config.min_content_length,
                "max_content_length": config.max_content_length,
                "min_title_length": config.min_title_length,
                "max_title_length": config.max_title_length,
                "date_required": config.date_required,
                "max_article_age_days": config.max_article_age_days,
                "enable_caching": config.enable_caching,
                "cache_ttl_hours": config.cache_ttl_hours,
                "use_rate_limiting": config.use_rate_limiting,
                "skip_duplicates": config.skip_duplicates,
                "require_summary": config.require_summary,
                "min_summary_length": config.min_summary_length,
                "respect_robots_txt": config.respect_robots_txt,
                "custom_user_agent": config.custom_user_agent,
                "custom_headers": config.custom_headers,
                "follow_pagination": config.follow_pagination,
                "max_pages": config.max_pages,
                "extract_full_content": config.extract_full_content,
                "continue_on_error": config.continue_on_error,
                "max_consecutive_errors": config.max_consecutive_errors,
                "enable_metrics": config.enable_metrics,
                "log_level": config.log_level,
            }
            return json.dumps(config_dict, indent=2)

        except Exception as e:
            logger.error("Failed to export config", domain=domain, error=str(e))
            return None

    def import_config(self, config_json: str) -> bool:
        """Import configuration from JSON"""
        try:
            config_dict = json.loads(config_json)
            domain = config_dict.get("domain")

            if not domain:
                logger.error("No domain specified in config")
                return False

            # Create config object
            config = ScraperConfig(**config_dict)

            # Validate
            issues = self.validate_config(config)
            if issues:
                logger.error("Config validation failed", domain=domain, issues=issues)
                return False

            # Store
            self.configs[domain] = config
            logger.info("Imported config", domain=domain)
            return True

        except Exception as e:
            logger.error("Failed to import config", error=str(e))
            return False

    def get_config_summary(self) -> Dict[str, Dict]:
        """Get summary of all configurations"""
        summary = {}

        for domain, config in self.configs.items():
            summary[domain] = {
                "max_articles": config.max_articles_per_run,
                "max_concurrent": config.max_concurrent_requests,
                "timeout": config.timeout_seconds,
                "cache_ttl": config.cache_ttl_hours,
                "date_required": config.date_required,
                "use_rate_limiting": config.use_rate_limiting,
                "enable_caching": config.enable_caching,
            }

        return summary

    def get_performance_optimized_config(self, domain: str) -> ScraperConfig:
        """Get performance-optimized configuration for a domain"""
        base_config = self.get_config(domain)

        # Create optimized copy
        optimized = ScraperConfig(
            domain=base_config.domain,
            max_articles_per_run=min(base_config.max_articles_per_run * 2, 100),
            max_concurrent_requests=min(base_config.max_concurrent_requests + 2, 8),
            timeout_seconds=max(base_config.timeout_seconds - 5, 15),
            retry_attempts=max(base_config.retry_attempts - 1, 1),
            retry_delay_seconds=base_config.retry_delay_seconds * 0.8,
            min_content_length=base_config.min_content_length,
            max_content_length=base_config.max_content_length,
            min_title_length=base_config.min_title_length,
            max_title_length=base_config.max_title_length,
            date_required=base_config.date_required,
            max_article_age_days=base_config.max_article_age_days,
            enable_caching=True,  # Always enable for performance
            cache_ttl_hours=base_config.cache_ttl_hours,
            use_rate_limiting=base_config.use_rate_limiting,
            skip_duplicates=True,  # Always skip for performance
            require_summary=base_config.require_summary,
            min_summary_length=base_config.min_summary_length,
            respect_robots_txt=base_config.respect_robots_txt,
            custom_user_agent=base_config.custom_user_agent,
            custom_headers=base_config.custom_headers,
            follow_pagination=base_config.follow_pagination,
            max_pages=min(base_config.max_pages, 3),  # Limit for performance
            extract_full_content=False,  # Disable for performance
            continue_on_error=True,  # Always continue for performance
            max_consecutive_errors=base_config.max_consecutive_errors,
            enable_metrics=base_config.enable_metrics,
            log_level=base_config.log_level,
        )

        logger.info("Generated performance-optimized config", domain=domain)
        return optimized


# Global config manager instance
_config_manager = ScraperConfigManager()


def get_config_manager() -> ScraperConfigManager:
    """Get the global config manager instance"""
    return _config_manager


def get_scraper_config(domain: str) -> ScraperConfig:
    """Get scraper configuration for a domain"""
    return _config_manager.get_config(domain)


if __name__ == "__main__":
    # Example usage
    config_manager = get_config_manager()

    # Get config for a domain
    config = config_manager.get_config("medicalxpress.com")
    print(f"Config for medicalxpress.com: {config}")

    # Update config
    config_manager.update_config("medicalxpress.com", max_articles_per_run=30)

    # Get summary
    summary = config_manager.get_config_summary()
    print(f"Config summary: {summary}")

    # Export config
    exported = config_manager.export_config("medicalxpress.com")
    print(f"Exported config: {exported}")

    # Get performance optimized config
    optimized = config_manager.get_performance_optimized_config("medicalxpress.com")
    print(f"Optimized config: {optimized}")
