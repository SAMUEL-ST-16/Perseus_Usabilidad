"""
Logging configuration for Perseus Backend
Provides centralized logging setup
"""

import logging
import sys
from typing import Optional
from app.core.config import settings


def setup_logger(
    name: str,
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance

    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages

    Returns:
        Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)

    # Set level
    log_level = level or settings.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    fmt = format_string or settings.LOG_FORMAT
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


# Default application logger
logger = setup_logger("perseus")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return setup_logger(name)
