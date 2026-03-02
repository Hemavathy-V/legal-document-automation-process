from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.sql_database import Base
import enum


# -----------------------------
# ENUMS
# -----------------------------

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class ActionType(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"


# -----------------------------
# MODELS
# -----------------------------

class Contract(Base):
    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)

    audit_logs = relationship("AuditLog", back_populates="contract")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    action_type = Column(String(50), nullable=False)

    contract = relationship("Contract", back_populates="audit_logs")