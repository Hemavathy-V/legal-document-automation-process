import os
import mysql.connector
from dotenv import load_dotenv
from backend.logger import get_logger

logger = get_logger(__name__)

load_dotenv()  # loads from project root

def get_connection():
    db_host = os.getenv("DATABASE_HOST")
    db_port = int(os.getenv("DATABASE_PORT", 3306))
    db_user = os.getenv("DATABASE_USER")
    db_name = os.getenv("DATABASE_NAME")
    
    logger.debug(f"Connecting to database: host={db_host}, port={db_port}, user={db_user}, db={db_name}")
    
    try:
        conn = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=os.getenv("DATABASE_PASSWORD"),
            database=db_name
        )
        logger.debug("Database connection established successfully")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise
