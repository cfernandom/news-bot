"""
Structured logging system for PreventIA News Analytics
Provides consistent, structured logging across all services
"""

import json
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class LogLevel(Enum):
    """Log levels for structured logging"""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class StructuredLogger:
    """
    Structured logger that outputs consistent JSON logs
    """

    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create structured handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)

        # Prevent duplicate logs
        self.logger.propagate = False

    def _log(self, level: LogLevel, message: str, **kwargs):
        """Internal logging method"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.value,
            "logger": self.name,
            "message": message,
            **kwargs,
        }

        # Use appropriate logging level
        log_method = getattr(self.logger, level.value)
        log_method(json.dumps(log_data))

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, **kwargs)

    # Specialized logging methods for common operations
    def scraper_started(self, domain: str, scraper_name: str, **kwargs):
        """Log scraper start"""
        self.info(
            "Scraper started",
            domain=domain,
            scraper_name=scraper_name,
            event_type="scraper_start",
            **kwargs,
        )

    def scraper_completed(
        self,
        domain: str,
        scraper_name: str,
        articles_found: int,
        execution_time: float,
        **kwargs,
    ):
        """Log scraper completion"""
        self.info(
            "Scraper completed successfully",
            domain=domain,
            scraper_name=scraper_name,
            articles_found=articles_found,
            execution_time=execution_time,
            event_type="scraper_success",
            **kwargs,
        )

    def scraper_failed(self, domain: str, scraper_name: str, error: str, **kwargs):
        """Log scraper failure"""
        self.error(
            "Scraper failed",
            domain=domain,
            scraper_name=scraper_name,
            error=error,
            event_type="scraper_failure",
            **kwargs,
        )

    def article_processed(
        self, title: str, url: str, domain: str, processing_time: float, **kwargs
    ):
        """Log article processing"""
        self.info(
            "Article processed",
            title=title[:100],  # Truncate long titles
            url=url,
            domain=domain,
            processing_time=processing_time,
            event_type="article_processed",
            **kwargs,
        )

    def date_parse_failed(self, date_str: str, article_url: str, domain: str, **kwargs):
        """Log date parsing failure"""
        self.warning(
            "Date parsing failed",
            date_str=date_str,
            article_url=article_url,
            domain=domain,
            event_type="date_parse_failure",
            **kwargs,
        )

    def compliance_check(
        self, domain: str, is_compliant: bool, violations: list, **kwargs
    ):
        """Log compliance check"""
        self.info(
            "Compliance check completed",
            domain=domain,
            is_compliant=is_compliant,
            violations=violations,
            event_type="compliance_check",
            **kwargs,
        )

    def pipeline_started(self, **kwargs):
        """Log pipeline start"""
        self.info("Pipeline started", event_type="pipeline_start", **kwargs)

    def pipeline_completed(self, total_articles: int, execution_time: float, **kwargs):
        """Log pipeline completion"""
        self.info(
            "Pipeline completed",
            total_articles=total_articles,
            execution_time=execution_time,
            event_type="pipeline_complete",
            **kwargs,
        )

    def performance_metric(
        self, metric_name: str, value: float, unit: str = "ms", **kwargs
    ):
        """Log performance metric"""
        self.info(
            f"Performance metric: {metric_name}",
            metric_name=metric_name,
            value=value,
            unit=unit,
            event_type="performance_metric",
            **kwargs,
        )


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs structured JSON logs
    """

    def format(self, record):
        # The message should already be JSON from StructuredLogger
        return record.getMessage()


# Global logger instances
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(name: str, level: str = "INFO") -> StructuredLogger:
    """
    Get or create a structured logger instance

    Args:
        name: Logger name (typically module name)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        StructuredLogger instance
    """
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name, level)
    return _loggers[name]


def configure_logging(level: str = "INFO"):
    """
    Configure global logging settings

    Args:
        level: Default log level for all loggers
    """
    # Set root logger level
    logging.getLogger().setLevel(getattr(logging, level.upper()))

    # Configure specific loggers
    for logger_name in ["scraper", "nlp", "orchestrator", "api"]:
        get_logger(logger_name, level)


# Convenience functions for common logging patterns
def log_scraper_metrics(
    logger: StructuredLogger,
    domain: str,
    scraper_name: str,
    articles_count: int,
    execution_time: float,
    success: bool,
):
    """Log scraper execution metrics"""
    if success:
        logger.scraper_completed(
            domain=domain,
            scraper_name=scraper_name,
            articles_found=articles_count,
            execution_time=execution_time,
        )
    else:
        logger.scraper_failed(
            domain=domain, scraper_name=scraper_name, error="Execution failed"
        )


def log_article_metrics(
    logger: StructuredLogger, articles: list, processing_time: float
):
    """Log article processing metrics"""
    for article in articles:
        logger.article_processed(
            title=article.title,
            url=article.url,
            domain=getattr(article, "domain", "unknown"),
            processing_time=processing_time / len(articles),
        )


# Example usage and configuration
if __name__ == "__main__":
    # Configure logging
    configure_logging("DEBUG")

    # Get logger
    logger = get_logger("test_module")

    # Test structured logging
    logger.info("System starting", component="test", version="1.0.0")
    logger.scraper_started("example.com", "test_scraper")
    logger.scraper_completed("example.com", "test_scraper", 15, 2.5)
    logger.warning("Low article count", domain="example.com", count=5)
    logger.error("Connection failed", domain="example.com", error="Timeout")
