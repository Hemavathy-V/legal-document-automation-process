import os
import mysql.connector
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

load_dotenv()  # loads from project root


def _read_env(primary_key: str, fallback_key: str | None = None, default: str | None = None) -> str | None:
    value = os.getenv(primary_key)
    if value is None and fallback_key:
        value = os.getenv(fallback_key)
    if value is None:
        return default
    return value.strip()

def get_connection():
    db_host = _read_env("MYSQL_HOST", "DATABASE_HOST")
    db_port = int(_read_env("MYSQL_PORT", "DATABASE_PORT", "3306"))
    db_user = _read_env("MYSQL_USER", "DATABASE_USER")
    db_password = _read_env("MYSQL_PASSWORD", "DATABASE_PASSWORD")
    db_name = _read_env("MYSQL_DB", "DATABASE_NAME")

    missing = [
        key for key, val in {
            "MYSQL_HOST": db_host,
            "MYSQL_USER": db_user,
            "MYSQL_PASSWORD": db_password,
            "MYSQL_DB": db_name,
        }.items() if not val
    ]

    if missing:
        message = f"Missing required database environment variables: {', '.join(missing)}"
        logger.error(message)
        raise RuntimeError(message)
    
    logger.debug(f"Connecting to database: host={db_host}, port={db_port}, user={db_user}, db={db_name}")
    
    try:
        conn = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        logger.debug("Database connection established successfully")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise
