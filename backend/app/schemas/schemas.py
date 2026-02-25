"""
Shared request/response schemas used across login, contracts, and templates.
"""
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr, field_validator


# --- Login / auth ---
class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class RegisterRequest(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    role: str

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    role: str


class UserUpdateRequest(BaseModel):
    """Admin update user: name, email, role; password optional (omit to keep current)."""
    user_name: str
    email: EmailStr
    password: Optional[str] = None
    role: str

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.strip().lower()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# --- Contracts ---
class ContractResponse(BaseModel):
    contract_id: int
    contract_type: str
    jurisdiction: str
    status: str
    created_by: str


# --- Templates ---
class TemplateResponse(BaseModel):
    id: int
    template_name: str
    template_type: str
    file_path: str


# --- Dynamic Contract Generation ---
class TemplatePlaceholdersResponse(BaseModel):
    """Response containing placeholders needed to fill a template"""
    template_name: str
    simple_fields: List[str]
    loop_fields: Dict[str, List[str]]


class ContractDataRequest(BaseModel):
    """Request payload with user-provided contract data"""
    template_name: str
    data: Dict[str, Any]


class ContractDataResponse(BaseModel):
    """Response after saving contract data"""
    message: str
    template_name: str
    file_path: str
    total_fields: int


class TemplateNamesResponse(BaseModel):
    """Response with available template names from DOCX files"""
    templates: List[str]
