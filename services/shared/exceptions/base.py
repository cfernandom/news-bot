"""
Base exception classes and error handling utilities for PreventIA News Analytics
"""

import asyncio
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Optional, Union

from services.shared.logging.structured_logger import get_logger

logger = get_logger("exceptions")


class PreventIAException(Exception):
    """
    Base exception class for all PreventIA-specific errors
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.original_exception = original_exception
        self.timestamp = datetime.now()

        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/API responses"""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "original_error": (
                str(self.original_exception) if self.original_exception else None
            ),
        }

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class ValidationException(PreventIAException):
    """Exception for data validation errors"""

    def __init__(self, field: str, value: Any, message: str, **kwargs):
        self.field = field
        self.value = value
        details = {"field": field, "value": str(value), **kwargs.get("details", {})}
        super().__init__(
            message=f"Validation failed for field '{field}': {message}",
            error_code="VALIDATION_ERROR",
            details=details,
            **kwargs,
        )


class ConfigurationException(PreventIAException):
    """Exception for configuration-related errors"""

    def __init__(self, config_key: str, message: str, **kwargs):
        self.config_key = config_key
        details = {"config_key": config_key, **kwargs.get("details", {})}
        super().__init__(
            message=f"Configuration error for '{config_key}': {message}",
            error_code="CONFIG_ERROR",
            details=details,
            **kwargs,
        )


class DatabaseException(PreventIAException):
    """Exception for database-related errors"""

    def __init__(self, operation: str, message: str, **kwargs):
        self.operation = operation
        details = {"operation": operation, **kwargs.get("details", {})}
        super().__init__(
            message=f"Database error during '{operation}': {message}",
            error_code="DATABASE_ERROR",
            details=details,
            **kwargs,
        )


class ScraperException(PreventIAException):
    """Exception for scraper-related errors"""

    def __init__(self, domain: str, scraper_name: str, message: str, **kwargs):
        self.domain = domain
        self.scraper_name = scraper_name
        details = {
            "domain": domain,
            "scraper_name": scraper_name,
            **kwargs.get("details", {}),
        }
        super().__init__(
            message=f"Scraper error for {domain} ({scraper_name}): {message}",
            error_code="SCRAPER_ERROR",
            details=details,
            **kwargs,
        )


class NLPException(PreventIAException):
    """Exception for NLP/AI processing errors"""

    def __init__(self, operation: str, message: str, **kwargs):
        self.operation = operation
        details = {"operation": operation, **kwargs.get("details", {})}
        super().__init__(
            message=f"NLP error during '{operation}': {message}",
            error_code="NLP_ERROR",
            details=details,
            **kwargs,
        )


class AuthenticationException(PreventIAException):
    """Exception for authentication errors"""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message=message, error_code="AUTH_ERROR", **kwargs)


class AuthorizationException(PreventIAException):
    """Exception for authorization/permission errors"""

    def __init__(self, resource: str, action: str, message: str = None, **kwargs):
        self.resource = resource
        self.action = action
        details = {"resource": resource, "action": action, **kwargs.get("details", {})}
        message = (
            message or f"Access denied for action '{action}' on resource '{resource}'"
        )
        super().__init__(
            message=message, error_code="AUTHORIZATION_ERROR", details=details, **kwargs
        )


class ExternalServiceException(PreventIAException):
    """Exception for external service integration errors"""

    def __init__(self, service: str, operation: str, message: str, **kwargs):
        self.service = service
        self.operation = operation
        details = {
            "service": service,
            "operation": operation,
            **kwargs.get("details", {}),
        }
        super().__init__(
            message=f"External service error ({service}/{operation}): {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details,
            **kwargs,
        )


class RateLimitException(PreventIAException):
    """Exception for rate limiting errors"""

    def __init__(
        self, resource: str, limit: int, reset_time: Optional[datetime] = None, **kwargs
    ):
        self.resource = resource
        self.limit = limit
        self.reset_time = reset_time
        details = {
            "resource": resource,
            "limit": limit,
            "reset_time": reset_time.isoformat() if reset_time else None,
            **kwargs.get("details", {}),
        }
        super().__init__(
            message=f"Rate limit exceeded for {resource} (limit: {limit})",
            error_code="RATE_LIMIT_ERROR",
            details=details,
            **kwargs,
        )


# Error logging utility
def log_exception(
    exception: Exception, context: Dict[str, Any] = None, level: str = "error"
) -> None:
    """
    Log an exception with structured context

    Args:
        exception: The exception to log
        context: Additional context information
        level: Log level (error, warning, critical)
    """
    context = context or {}

    if isinstance(exception, PreventIAException):
        # Log PreventIA exceptions with full context
        log_data = {
            "exception_type": exception.__class__.__name__,
            "error_code": exception.error_code,
            "message": exception.message,
            "details": exception.details,
            "timestamp": exception.timestamp.isoformat(),
            **context,
        }

        if exception.original_exception:
            log_data["original_error"] = str(exception.original_exception)
            log_data["traceback"] = traceback.format_exception(
                type(exception.original_exception),
                exception.original_exception,
                exception.original_exception.__traceback__,
            )
    else:
        # Log standard exceptions
        log_data = {
            "exception_type": exception.__class__.__name__,
            "message": str(exception),
            "traceback": traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ),
            **context,
        }

    # Log with appropriate level
    log_method = getattr(logger, level, logger.error)
    log_method("Exception occurred", **log_data)


# Error handler decorator
def error_handler(
    exceptions: Union[Exception, tuple] = Exception,
    default_return=None,
    reraise: bool = False,
    log_level: str = "error",
):
    """
    Decorator for standardized error handling

    Args:
        exceptions: Exception types to catch
        default_return: Default return value on error
        reraise: Whether to reraise the exception after logging
        log_level: Log level for caught exceptions
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                log_exception(
                    e,
                    context={
                        "function": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs),
                    },
                    level=log_level,
                )

                if reraise:
                    raise
                return default_return

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                log_exception(
                    e,
                    context={
                        "function": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs),
                    },
                    level=log_level,
                )

                if reraise:
                    raise
                return default_return

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


# Specific error handlers for common operations
def handle_database_error(operation: str):
    """Decorator for database operation error handling"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Convert to DatabaseException
                raise DatabaseException(
                    operation=operation,
                    message=str(e),
                    original_exception=e,
                    details={"function": func.__name__},
                )

        return wrapper

    return decorator


def handle_scraper_error(domain: str, scraper_name: str):
    """Decorator for scraper operation error handling"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Convert to ScraperException
                raise ScraperException(
                    domain=domain,
                    scraper_name=scraper_name,
                    message=str(e),
                    original_exception=e,
                    details={"function": func.__name__},
                )

        return wrapper

    return decorator


def handle_api_error(reraise: bool = True):
    """Decorator for API endpoint error handling"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except PreventIAException:
                # Re-raise our custom exceptions
                raise
            except Exception as e:
                log_exception(
                    e,
                    context={
                        "endpoint": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs),
                    },
                )

                if reraise:
                    raise

                # Return error response
                return {
                    "error": True,
                    "message": "Internal server error",
                    "details": (
                        str(e)
                        if isinstance(e, (ValidationException, ConfigurationException))
                        else None
                    ),
                }

        return wrapper

    return decorator


# Context manager for error handling
class ErrorContext:
    """Context manager for structured error handling"""

    def __init__(self, operation: str, context: Dict[str, Any] = None):
        self.operation = operation
        self.context = context or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        logger.debug(f"Starting operation: {self.operation}", **self.context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = (datetime.now() - self.start_time).total_seconds()

        if exc_type is None:
            logger.debug(
                f"Operation completed: {self.operation}",
                execution_time=execution_time,
                **self.context,
            )
        else:
            log_exception(
                exc_val,
                context={
                    "operation": self.operation,
                    "execution_time": execution_time,
                    **self.context,
                },
            )

        return False  # Don't suppress exceptions


if __name__ == "__main__":
    # Example usage

    # Test custom exceptions
    try:
        raise ValidationException("email", "invalid-email", "Invalid email format")
    except ValidationException as e:
        print("Validation error:", e.to_dict())

    # Test error handler decorator
    @error_handler(exceptions=ValueError, default_return="Error occurred")
    def test_function(value):
        if value < 0:
            raise ValueError("Value must be positive")
        return value * 2

    result = test_function(-5)
    print(f"Function result: {result}")

    # Test context manager
    with ErrorContext("test_operation", {"param": "value"}):
        print("Operation in progress...")
        # raise Exception("Test error")  # Uncomment to test error handling
