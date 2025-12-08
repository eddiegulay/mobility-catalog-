"""Logging configuration for the application."""

import logging
import sys
from config.settings import settings


def setup_logger(name: str = "langgraph_agent") -> logging.Logger:
    """
    Set up and configure a logger with color-coded output.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level based on DEBUG setting
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format: [LEVEL] timestamp - message
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Default logger instance
logger = setup_logger()
