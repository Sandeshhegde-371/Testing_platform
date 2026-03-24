"""
app/core/logging.py

Structured logging configuration using structlog.

Provides:
    - configure_logging()  : call once at startup to initialise the logging pipeline
    - get_logger(name)     : get a bound logger for a specific module
    - RequestIDFilter      : inject request-id into every log record

Log output format:
    - Development : pretty-printed key-value pairs (human readable)
    - Production  : JSON lines (machine parseable, ingested by Datadog / CloudWatch)

Usage:
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("test_case.created", test_case_id="TC-001", user_id="u1")
"""

import logging
from typing import Optional


def configure_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """
    Initialise structlog and standard library logging.

    Args:
        log_level:  Minimum log level (DEBUG | INFO | WARNING | ERROR | CRITICAL).
        log_format: Output format - "json" for production, "text" for development.

    Should be called once during application startup (inside lifespan).
    """
    pass


def get_logger(name: Optional[str] = None):
    """
    Return a bound structlog logger for the given module name.

    Args:
        name: Module name, typically __name__. Defaults to root logger.

    Returns:
        BoundLogger: A structlog bound logger instance.

    Example:
        logger = get_logger(__name__)
        logger.info("event", key="value")
    """
    pass


class RequestIDFilter(logging.Filter):
    """
    Logging filter that injects the current request ID into every log record.

    Added to the root handler so that all log lines within a request context
    carry the same request_id for distributed tracing correlation.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Attach request_id context variable to the log record."""
        pass
