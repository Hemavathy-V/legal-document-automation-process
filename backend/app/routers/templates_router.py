"""
Templates feature: list contract templates endpoint.
Route: GET /api/templates
"""
from typing import List

from fastapi import APIRouter, Depends

from backend.app.deps import get_current_user
from backend.app.schemas import TemplateResponse, UserResponse
from database.db_connection import get_connection


router = APIRouter(tags=["templates"])


@router.get("/templates", response_model=List[TemplateResponse])
def list_templates(current_user: UserResponse = Depends(get_current_user)):
    """
    List all contract templates from contract_templates table.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, template_name, template_type, file_path
            FROM contract_templates
            ORDER BY id
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
