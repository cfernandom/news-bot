"""
Context management for structured logging
Provides thread-local context storage for request tracking
"""

import threading
from contextvars import ContextVar
from typing import Any, Dict, Optional
from uuid import uuid4

# Context variable for async contexts
_log_context: ContextVar[Dict[str, Any]] = ContextVar("log_context", default={})

# Thread-local storage for sync contexts
_thread_local = threading.local()


class LogContext:
    """Context manager for logging context"""

    @classmethod
    def get_context(cls) -> Dict[str, Any]:
        """Get current logging context"""
        try:
            # Try async context first
            return _log_context.get({})
        except:
            # Fall back to thread-local
            return getattr(_thread_local, "context", {})

    @classmethod
    def set_context(cls, context: Dict[str, Any]) -> None:
        """Set logging context"""
        try:
            # Try async context first
            _log_context.set(context)
        except:
            # Fall back to thread-local
            _thread_local.context = context

    @classmethod
    def add_to_context(cls, **kwargs: Any) -> None:
        """Add items to current context"""
        current = cls.get_context().copy()
        current.update(kwargs)
        cls.set_context(current)

    @classmethod
    def clear_context(cls) -> None:
        """Clear logging context"""
        cls.set_context({})

    def __init__(self, **context: Any):
        """Initialize context manager with context data"""
        self.context = context
        self.previous_context = None

    def __enter__(self):
        """Enter context manager"""
        self.previous_context = self.get_context()
        new_context = self.previous_context.copy()
        new_context.update(self.context)
        self.set_context(new_context)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager"""
        if self.previous_context is not None:
            self.set_context(self.previous_context)
        else:
            self.clear_context()


# Convenience functions
def add_context(**kwargs: Any) -> None:
    """Add context to current logging context"""
    LogContext.add_to_context(**kwargs)


def clear_context() -> None:
    """Clear current logging context"""
    LogContext.clear_context()


def with_request_id(request_id: Optional[str] = None) -> LogContext:
    """Create context with request ID"""
    if request_id is None:
        request_id = str(uuid4())
    return LogContext(request_id=request_id)


def with_user_context(user_id: str, email: Optional[str] = None) -> LogContext:
    """Create context with user information"""
    context = {"user_id": user_id}
    if email:
        context["user_email"] = email
    return LogContext(**context)


def with_operation_context(operation: str, **kwargs: Any) -> LogContext:
    """Create context for a specific operation"""
    context = {"operation": operation}
    context.update(kwargs)
    return LogContext(**context)
