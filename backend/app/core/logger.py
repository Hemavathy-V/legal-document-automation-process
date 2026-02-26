"""
Centralized logging configuration for the Legal Document Automation System.
All modules import logger from this file for consistent logging across the application.

Updated: Removed contract_ai module references.
Currently logging:
  - Backend API (FastAPI, routers, authentication)
  - Database operations
  - Template processing (fetch/ingest)
"""
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths - Single log file per application session
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
ERROR_LOG_FILE = LOGS_DIR / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Logger configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    
    Features:
        - Console output: INFO level and above
        - File output: DEBUG level and above (rotating 10MB files, 5 backups)
        - Error file: ERROR level and above (rotating 10MB files, 3 backups)
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # ============================================
    # Console Handler (INFO and above)
    # ============================================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # ============================================
    # File Handler (DEBUG and above) - All logs
    # ============================================
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # ============================================
    # Error File Handler (ERROR and above)
    # ============================================
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)
    
    return logger


# ============================================
# Root logger initialization
# ============================================
root_logger = get_logger(__name__)

# Log application startup information
root_logger.info("=" * 80)
root_logger.info("Legal Document Automation System - Logging Initialized")
root_logger.info(f"Log directory: {LOGS_DIR}")
root_logger.info(f"Main log file: {LOG_FILE}")
root_logger.info(f"Error log file: {ERROR_LOG_FILE}")
root_logger.info("=" * 80)
root_logger.debug("Logging system ready. All modules can now use get_logger(__name__)")
