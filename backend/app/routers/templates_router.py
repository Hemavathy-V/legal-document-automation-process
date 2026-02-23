"""
Templates feature: list contract templates endpoint.
Route: GET /api/templates
"""
from typing import List

from fastapi import APIRouter, Depends

from backend.app.deps import get_current_user
from backend.app.schemas import TemplateResponse, UserResponse
from backend.database.db_connection import get_connection
from backend.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["templates"])


@router.get("/templates", response_model=List[TemplateResponse])
def list_templates(current_user: UserResponse = Depends(get_current_user)):
    """
    List all contract templates from contract_templates table.
    """
    logger.info(f"User {current_user.user_name} (ID: {current_user.user_id}) requested templates list")
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        logger.debug("Fetching templates from database")
        cursor.execute(
            """
            SELECT id, template_name, template_type, file_path
            FROM contract_templates
            ORDER BY id
            """
        )
        templates = cursor.fetchall()
        logger.info(f"Retrieved {len(templates)} templates from database")
        return templates
    except Exception as e:
        logger.error(f"Error fetching templates: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()
        logger.debug("Database connection closed")
