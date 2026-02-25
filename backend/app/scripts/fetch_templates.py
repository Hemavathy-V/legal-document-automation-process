"""
Utility script: fetch contract template files from the database record list
and copy them into the project-level output/ folder.

Usage:
    python -m backend.scripts.fetch_templates
    # or from project root:
    python backend/scripts/fetch_templates.py
"""
import os
import shutil
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_PROJECT_ROOT / ".env", override=True)

from backend.app.core.logger import get_logger  # noqa: E402 – after sys.path is set

logger = get_logger(__name__)

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 3306))
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

OUTPUT_FOLDER = _PROJECT_ROOT / "output"


def fetch_templates_from_db():
    """
    Fetch contract templates from MySQL and copy the source files into output/.
    """
    logger.info("Starting template fetch operation")
    logger.debug(f"Output folder: {OUTPUT_FOLDER}")

    try:
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output folder ready: {OUTPUT_FOLDER}")

        logger.debug(f"Connecting to database: {DATABASE_HOST}:{DATABASE_PORT}")
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
        )
        logger.info("Database connection established")

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, template_name, template_type, file_path FROM contract_templates"
        )
        templates = cursor.fetchall()

        if not templates:
            logger.warning("No templates found in database")
            cursor.close()
            connection.close()
            return

        logger.info(f"Found {len(templates)} templates in database")

        for template in templates:
            template_id = template["id"]
            template_name = template["template_name"]
            template_type = template["template_type"]
            file_path = template["file_path"]

            logger.debug(
                f"Processing template {template_id}: {template_name} (type: {template_type})"
            )

            full_source_path = _PROJECT_ROOT / file_path

            if not full_source_path.exists():
                logger.warning(
                    f"Template {template_id} ({template_name}): "
                    f"File not found at {full_source_path}"
                )
                continue

            destination_path = OUTPUT_FOLDER / Path(file_path).name

            try:
                shutil.copy2(full_source_path, destination_path)
                logger.info(
                    f"Template {template_id} ({template_name}): "
                    f"Successfully copied to {destination_path}"
                )
            except Exception as e:
                logger.error(
                    f"Template {template_id} ({template_name}): "
                    f"Error copying file - {str(e)}"
                )

        cursor.close()
        connection.close()
        logger.info(
            f"Template fetch completed. Templates saved to: {OUTPUT_FOLDER}"
        )

    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in template fetch: {str(e)}")
        raise


if __name__ == "__main__":
    fetch_templates_from_db()
