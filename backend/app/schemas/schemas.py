"""
Shared request/response schemas used across login, contracts, and templates.
"""
from typing import List, Dict, Any

from pydantic import BaseModel


# --- Login / auth ---
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    user_name: str
    email: str
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    role: str


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
