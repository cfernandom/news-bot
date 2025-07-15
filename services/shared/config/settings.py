"""
Centralized configuration management for PreventIA News Analytics
Uses Pydantic Settings for unified configuration across all services
"""

import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Environment types"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseSettings(BaseSettings):
    """Database configuration"""

    url: str = Field(
        "postgresql://preventia:preventia123@localhost:5433/preventia_news",
        env="DATABASE_URL",
    )
    pool_size: int = Field(5, env="DB_POOL_SIZE")
    max_overflow: int = Field(10, env="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(30, env="DB_POOL_TIMEOUT")
    pool_recycle: int = Field(3600, env="DB_POOL_RECYCLE")
    echo: bool = Field(False, env="DB_ECHO")

    @validator("url")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v


class RedisSettings(BaseSettings):
    """Redis configuration"""

    url: str = Field("redis://localhost:6379", env="REDIS_URL")
    db: int = Field(1, env="REDIS_DB")
    pool_size: int = Field(10, env="REDIS_POOL_SIZE")
    timeout: int = Field(5, env="REDIS_TIMEOUT")


class APISettings(BaseSettings):
    """API configuration"""

    host: str = Field("0.0.0.0", env="API_HOST")
    port: int = Field(8000, env="API_PORT")
    reload: bool = Field(False, env="API_RELOAD")
    cors_origins: list = Field(["*"], env="API_CORS_ORIGINS")

    # Security
    jwt_secret_key: str = Field(
        "your-development-secret-key-change-in-production-minimum-32-characters",
        env="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(24, env="JWT_EXPIRATION_HOURS")

    @validator("jwt_secret_key")
    def validate_jwt_secret(cls, v):
        if not v:
            raise ValueError("JWT_SECRET_KEY must be set")
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long")
        return v


class ScraperSettings(BaseSettings):
    """Scraper configuration"""

    max_concurrent_scrapers: int = Field(5, env="SCRAPER_MAX_CONCURRENT")
    default_timeout: int = Field(30, env="SCRAPER_DEFAULT_TIMEOUT")
    default_retry_attempts: int = Field(3, env="SCRAPER_DEFAULT_RETRY_ATTEMPTS")
    default_retry_delay: float = Field(1.0, env="SCRAPER_DEFAULT_RETRY_DELAY")

    # Content requirements (business rules)
    require_date: bool = Field(True, env="SCRAPER_REQUIRE_DATE")
    require_summary: bool = Field(True, env="SCRAPER_REQUIRE_SUMMARY")
    require_title: bool = Field(True, env="SCRAPER_REQUIRE_TITLE")

    min_title_length: int = Field(10, env="SCRAPER_MIN_TITLE_LENGTH")
    max_title_length: int = Field(200, env="SCRAPER_MAX_TITLE_LENGTH")
    min_summary_length: int = Field(20, env="SCRAPER_MIN_SUMMARY_LENGTH")
    min_content_length: int = Field(
        0, env="SCRAPER_MIN_CONTENT_LENGTH"
    )  # 0 for metadata-only

    # Performance
    enable_caching: bool = Field(True, env="SCRAPER_ENABLE_CACHING")
    cache_ttl_hours: int = Field(24, env="SCRAPER_CACHE_TTL_HOURS")
    enable_rate_limiting: bool = Field(True, env="SCRAPER_ENABLE_RATE_LIMITING")

    # Compliance
    respect_robots_txt: bool = Field(True, env="SCRAPER_RESPECT_ROBOTS_TXT")
    default_user_agent: str = Field(
        "PreventIA-Research-Bot/1.0 (Academic Research; UCOMPENSAR)",
        env="SCRAPER_DEFAULT_USER_AGENT",
    )


class NLPSettings(BaseSettings):
    """NLP configuration"""

    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    max_tokens: int = Field(1000, env="NLP_MAX_TOKENS")
    temperature: float = Field(0.1, env="NLP_TEMPERATURE")

    # Decision engine
    publish_threshold: int = Field(2, env="DECISION_PUBLISH_THRESHOLD")

    @validator("openai_api_key")
    def validate_openai_key(cls, v, values):
        # Allow test keys in development/testing
        environment = os.getenv("ENVIRONMENT", "development")
        if v and v.startswith("test_") and environment == "production":
            raise ValueError("OpenAI API key appears to be a test key in production")
        return v


class PublisherSettings(BaseSettings):
    """Publisher configuration"""

    wordpress_url: Optional[str] = Field(None, env="WORDPRESS_URL")
    wordpress_username: Optional[str] = Field(None, env="WORDPRESS_USERNAME")
    wordpress_password: Optional[str] = Field(None, env="WORDPRESS_PASSWORD")
    wordpress_feature_image_id: Optional[str] = Field(
        None, env="WORDPRESS_FEATURE_IMAGE_ID"
    )


class MonitoringSettings(BaseSettings):
    """Monitoring and logging configuration"""

    log_level: LogLevel = Field(LogLevel.INFO, env="LOG_LEVEL")
    enable_structured_logging: bool = Field(True, env="ENABLE_STRUCTURED_LOGGING")
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    metrics_port: int = Field(9090, env="METRICS_PORT")

    # Performance monitoring
    enable_performance_tracking: bool = Field(True, env="ENABLE_PERFORMANCE_TRACKING")
    performance_retention_days: int = Field(7, env="PERFORMANCE_RETENTION_DAYS")


class Settings(BaseSettings):
    """Main application settings"""

    # Environment
    environment: Environment = Field(Environment.DEVELOPMENT, env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")

    # Service configurations
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    api: APISettings = APISettings()
    scraper: ScraperSettings = ScraperSettings()
    nlp: NLPSettings = NLPSettings()
    publisher: PublisherSettings = PublisherSettings()
    monitoring: MonitoringSettings = MonitoringSettings()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env

    @validator("environment")
    def validate_environment_specific_settings(cls, v, values):
        """Validate environment-specific requirements"""
        if v == Environment.PRODUCTION:
            # Production validations
            if values.get("debug", False):
                raise ValueError("DEBUG must be False in production")

            api_settings = values.get("api")
            if api_settings and (
                not api_settings.jwt_secret_key
                or api_settings.jwt_secret_key == "your-secret-key-change-in-production"
            ):
                raise ValueError("JWT_SECRET_KEY must be set for production")

        return v

    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == Environment.PRODUCTION

    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.environment == Environment.TESTING


# Global settings instance
settings = Settings()


# Helper functions for backward compatibility
def get_database_url() -> str:
    """Get database URL"""
    return settings.database.url


def get_redis_url() -> str:
    """Get Redis URL"""
    return settings.redis.url


def get_jwt_secret() -> str:
    """Get JWT secret key"""
    return settings.api.jwt_secret_key


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key"""
    return settings.nlp.openai_api_key


def get_log_level() -> str:
    """Get log level"""
    return settings.monitoring.log_level.value


def get_scraper_settings() -> ScraperSettings:
    """Get scraper settings"""
    return settings.scraper


# Environment validation on import
if __name__ == "__main__":
    # Validate settings
    try:
        settings = Settings()
        print("✅ Configuration validated successfully")
        print(f"Environment: {settings.environment}")
        print(f"Database: {settings.database.url[:20]}...")
        print(f"Redis: {settings.redis.url}")
        print(f"API: {settings.api.host}:{settings.api.port}")
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        exit(1)
