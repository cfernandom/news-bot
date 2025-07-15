"""
Centralized configuration management for PreventIA News Analytics
"""

from .settings import (
    APISettings,
    DatabaseSettings,
    Environment,
    LogLevel,
    MonitoringSettings,
    NLPSettings,
    PublisherSettings,
    RedisSettings,
    ScraperSettings,
    Settings,
    get_database_url,
    get_jwt_secret,
    get_log_level,
    get_openai_api_key,
    get_redis_url,
    get_scraper_settings,
    settings,
)

__all__ = [
    "settings",
    "get_database_url",
    "get_redis_url",
    "get_jwt_secret",
    "get_openai_api_key",
    "get_log_level",
    "get_scraper_settings",
    "Environment",
    "LogLevel",
    "DatabaseSettings",
    "RedisSettings",
    "APISettings",
    "ScraperSettings",
    "NLPSettings",
    "PublisherSettings",
    "MonitoringSettings",
    "Settings",
]
