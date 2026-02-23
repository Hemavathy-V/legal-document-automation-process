import os
import shutil
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv
import sys

# Add backend to path for logger import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from backend.logger import get_logger

logger = get_logger(__name__)

# Load environment variables from repo root .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'), override=True)

# Get MySQL credentials from .env
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

logger.debug(
    f"MySQL configuration loaded | host={MYSQL_HOST} | port={MYSQL_PORT} | "
    f"user_set={bool(MYSQL_USER)} | db_set={bool(MYSQL_DB)}"
)

# Define output folder path
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
# Project root is one level above backend/
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')


def fetch_templates_from_db():
    """
    Fetch contract templates from MySQL database and save them to output folder
    """
    logger.info("Starting template fetch operation")
    logger.debug(f"Output folder: {OUTPUT_FOLDER}")
    logger.debug(f"Project root: {PROJECT_ROOT}")
    
    connection = None
    cursor = None

    try:
        # Create output folder if it doesn't exist
        Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output folder ready: {OUTPUT_FOLDER}")
        
        # Connect to MySQL database
        logger.debug(f"Connecting to database: {MYSQL_HOST}:{MYSQL_PORT}")
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        logger.info("Database connection established")
        
        cursor = connection.cursor(dictionary=True)
        
        # Fetch all contract templates from database
        logger.debug("Fetching templates from database")
        query = "SELECT id, template_name, template_type, file_path FROM contract_templates"
        cursor.execute(query)
        templates = cursor.fetchall()
        
        if not templates:
            logger.warning("No templates found in database")
            return
        
        logger.info(f"Found {len(templates)} templates in database")
        
        # Process each template
        for template in templates:
            template_id = template['id']
            template_name = template['template_name']
            template_type = template['template_type']
            file_path = template['file_path']
            
            logger.debug(f"Processing template {template_id}: {template_name} (type: {template_type})")
            
            # Construct full file path
            full_source_path = os.path.join(PROJECT_ROOT, file_path)
            
            # Check if source file exists
            if not os.path.exists(full_source_path):
                logger.warning(f"Template {template_id} ({template_name}): File not found at {full_source_path}")
                continue
            
            # Create destination path
            destination_path = os.path.join(OUTPUT_FOLDER, os.path.basename(file_path))
            
            try:
                # Copy file to output folder
                shutil.copy2(full_source_path, destination_path)
                logger.info(f"Template {template_id} ({template_name}): Successfully copied to {destination_path}")
            except Exception as e:
                logger.error(f"Template {template_id} ({template_name}): Error copying file - {str(e)}")
        
        logger.info(f"Template fetch operation completed. Templates saved to: {OUTPUT_FOLDER}")
        
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in template fetch: {str(e)}", exc_info=True)
        raise
    finally:
        if cursor:
            cursor.close()
            logger.debug("Database cursor closed")
        if connection and connection.is_connected():
            connection.close()
            logger.debug("Database connection closed")


if __name__ == "__main__":
    fetch_templates_from_db()
