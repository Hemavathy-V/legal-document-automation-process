"""
Shared request/response schemas used across login, contracts, and templates.
"""
from typing import List

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
