"""
Centralized exception handling for PreventIA News Analytics
Provides consistent error handling patterns across all services
"""

from .base import (
    AuthenticationException,
    AuthorizationException,
    ConfigurationException,
    DatabaseException,
    ExternalServiceException,
    NLPException,
    PreventIAException,
    RateLimitException,
    ScraperException,
    ValidationException,
    error_handler,
    handle_api_error,
    handle_database_error,
    handle_scraper_error,
    log_exception,
)

__all__ = [
    "PreventIAException",
    "ValidationException",
    "ConfigurationException",
    "DatabaseException",
    "ScraperException",
    "NLPException",
    "AuthenticationException",
    "AuthorizationException",
    "ExternalServiceException",
    "RateLimitException",
    "error_handler",
    "log_exception",
    "handle_database_error",
    "handle_scraper_error",
    "handle_api_error",
]
