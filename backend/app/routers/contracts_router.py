"""
Contracts feature: list contracts endpoint.
Route: GET /api/contracts
"""
from typing import List

from fastapi import APIRouter, Depends

from backend.app.deps import get_current_user
from backend.app.schemas import ContractResponse, UserResponse
from database.db_connection import get_connection


router = APIRouter(tags=["contracts"])


@router.get("/contracts", response_model=List[ContractResponse])
def list_contracts(current_user: UserResponse = Depends(get_current_user)):
    """
    List all contracts with type, jurisdiction, status and creator.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                c.contract_id,
                ct.lookup_value AS contract_type,
                j.lookup_value AS jurisdiction,
                s.lookup_value AS status,
                u.user_name AS created_by
            FROM contracts c
            JOIN look_up ct ON c.contract_type_id = ct.lookup_id
            JOIN look_up j ON c.jurisdiction_id = j.lookup_id
            JOIN look_up s ON c.status_id = s.lookup_id
            JOIN users u ON c.created_by = u.user_id
            ORDER BY c.contract_id
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
