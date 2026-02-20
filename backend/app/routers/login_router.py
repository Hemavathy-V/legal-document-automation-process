"""
Login feature: login and register endpoints.
Routes: POST /api/login, POST /api/register
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from backend.app.auth import create_access_token
from backend.app.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from database.db_connection import get_connection


router = APIRouter(tags=["login"])


@router.options("/login")
def login_options():
    """CORS preflight for POST /api/login."""
    return {}


def _get_user_by_email(email: str) -> Optional[dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                u.user_id,
                u.user_name,
                u.email,
                u.password,
                r.lookup_value AS role
            FROM users u
            JOIN look_up r ON u.role_id = r.lookup_id
            WHERE u.email = %s
            """,
            (email,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Login with email and password. Returns JWT and user info.
    """
    user_row = _get_user_by_email(request.email)
    if not user_row or not user_row.get("password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if request.password != user_row["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user = UserResponse(
        user_id=user_row["user_id"],
        user_name=user_row["user_name"],
        email=user_row["email"],
        role=user_row["role"],
    )
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token, user=user)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    """
    Register a new user with password and role.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT user_id FROM users WHERE email = %s", (request.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        cursor.execute(
            """
            SELECT lookup_id
            FROM look_up
            WHERE lookup_type = 'user_role' AND lookup_value = %s
            """,
            (request.role,),
        )
        role_row = cursor.fetchone()
        if not role_row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            )

        cursor.execute(
            """
            INSERT INTO users (user_name, role_id, email, password)
            VALUES (%s, %s, %s, %s)
            """,
            (request.user_name, role_row["lookup_id"], request.email, request.password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        return UserResponse(
            user_id=user_id,
            user_name=request.user_name,
            email=request.email,
            role=request.role,
        )
    finally:
        cursor.close()
        conn.close()
