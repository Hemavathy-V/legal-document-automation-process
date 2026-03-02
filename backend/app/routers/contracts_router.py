"""
Contracts feature: list contracts endpoint.
Route: GET /api/contracts
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.app.deps.deps import get_current_user
from backend.app.schemas.schemas import ContractResponse, UserResponse
from backend.app.database.db_connection import get_connection
from backend.app.core.logger import get_logger

from sqlalchemy.orm import Session
from backend.app.database.sql_database import SessionLocal
from backend.app.models.db_models import Contract, AuditLog, ActionType
from backend.app.schemas.schemas import ContractCreate, ContractEdit, AuditLogResponse
from backend.app.utils.diff_utils import generate_diff

logger = get_logger(__name__)

router = APIRouter(tags=["contracts"])


@router.get("/contracts", response_model=List[ContractResponse])
def list_contracts(current_user: UserResponse = Depends(get_current_user)):
    """
    List contracts. Admins see all contracts; other roles see only their own.
    """
    is_admin = current_user.role == "Admin"
    logger.info(
        f"User {current_user.user_name} (ID: {current_user.user_id}, role: {current_user.role}) "
        f"requested contracts list — {'all' if is_admin else 'own only'}"
    )
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        base_query = """
            SELECT
                c.contract_id,
                ct.lookup_value AS contract_type,
                j.lookup_value  AS jurisdiction,
                s.lookup_value  AS status,
                u.user_name     AS created_by
            FROM contracts c
            JOIN look_up ct ON c.contract_type_id = ct.lookup_id
            JOIN look_up j  ON c.jurisdiction_id  = j.lookup_id
            JOIN look_up s  ON c.status_id         = s.lookup_id
            JOIN users u    ON c.created_by        = u.user_id
        """

        if is_admin:
            cursor.execute(base_query + " ORDER BY c.contract_id")
        else:
            cursor.execute(
                base_query + " WHERE c.created_by = %s ORDER BY c.contract_id",
                (current_user.user_id,),
            )

        contracts = cursor.fetchall()
        logger.info(f"Retrieved {len(contracts)} contracts for {current_user.user_name}")
        return contracts
    except Exception as e:
        logger.error(f"Error fetching contracts: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Create Contract
@router.post("/contracts")
def create_contract(data: ContractCreate, db: Session = Depends(get_db)):
    contract = Contract(
        title=data.title,
        content=data.content,
        created_by=data.created_by
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)

    audit = AuditLog(
        contract_id=contract.id,
        user_id=data.created_by,
        user_role="PARTY_1",
        action_type=ActionType.CREATE,
        old_content=None,
        new_content=data.content,
        change_summary="Initial contract creation"
    )

    db.add(audit)
    db.commit()

    return {"message": "Contract created", "contract_id": contract.id}


# ✅ Edit Contract (Manual or AI)
@router.put("/contracts/{contract_id}")
def edit_contract(contract_id: int, data: ContractEdit, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    old_content = contract.content
    new_content = data.new_content

    diff_summary = generate_diff(old_content, new_content)

    action_type = ActionType.AI_EDIT if data.is_ai else ActionType.EDIT

    audit = AuditLog(
        contract_id=contract_id,
        user_id=data.user_id,
        user_role=data.user_role,
        action_type=action_type,
        old_content=old_content,
        new_content=new_content,
        change_summary=diff_summary
    )

    db.add(audit)

    contract.content = new_content
    db.commit()

    return {"message": "Contract updated successfully"}


# ✅ Get Audit Logs
@router.get("/contracts/{contract_id}/audit-logs", response_model=list[AuditLogResponse])
def get_audit_logs(contract_id: int, db: Session = Depends(get_db)):
    logs = db.query(AuditLog)\
        .filter(AuditLog.contract_id == contract_id)\
        .order_by(AuditLog.created_at.desc())\
        .all()

    return logs