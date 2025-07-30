"""
Custom formatters for structured logging
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def __init__(self, config):
        super().__init__()
        self.config = config

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add service information if configured
        if self.config.include_service:
            log_data["service"] = getattr(record, "service", self.config.service_name)
            log_data["version"] = self.config.version
            log_data["environment"] = self.config.environment

        # Add extra fields from the record
        if hasattr(record, "extra") and record.extra:
            log_data.update(record.extra)

        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add stack info if present
        if record.stack_info:
            log_data["stack_info"] = record.stack_info

        return json.dumps(log_data, default=str, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter"""

    def __init__(self, config):
        super().__init__()
        self.config = config

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for console output"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        service = getattr(record, "service", self.config.service_name)

        # Build the base message
        base_msg = f"[{timestamp}] {record.levelname:<8} {service}:{record.name} - {record.getMessage()}"

        # Add extra context if available
        if hasattr(record, "extra") and record.extra:
            context_parts = []
            for key, value in record.extra.items():
                if key not in ["service", "timestamp", "environment", "version"]:
                    context_parts.append(f"{key}={value}")

            if context_parts:
                base_msg += f" | {' '.join(context_parts)}"

        # Add exception information if present
        if record.exc_info:
            base_msg += f"\n{self.formatException(record.exc_info)}"

        return base_msg
