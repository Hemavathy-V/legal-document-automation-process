"""
Shared dependencies (e.g. current user from JWT) for protected routes.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.app.auth import decode_token
from backend.app.schemas import UserResponse
from database.db_connection import get_connection


# Use /token for OpenAPI docs only; actual login is POST /api/login with JSON
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=True)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                u.user_id,
                u.user_name,
                u.email,
                r.lookup_value AS role
            FROM users u
            JOIN look_up r ON u.role_id = r.lookup_id
            WHERE u.email = %s
            """,
            (email,),
        )
        row = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserResponse(
        user_id=row["user_id"],
        user_name=row["user_name"],
        email=row["email"],
        role=row["role"],
    )
