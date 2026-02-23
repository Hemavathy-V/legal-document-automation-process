"""
Shared dependencies (e.g. current user from JWT) for protected routes.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth import decode_token
from app.schemas import UserResponse
from database.db_connection import get_connection
from app.core.logger import get_logger

logger = get_logger(__name__)


# Use /token for OpenAPI docs only; actual login is POST /api/login with JSON
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=True)


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    logger.debug("Validating current user from token")
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Invalid token payload: no email found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
    except ValueError as e:
        logger.error(f"Token validation failed: {str(e)}")
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
        logger.warning(f"User not found for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    logger.info(f"User authenticated successfully: {email} (ID: {row['user_id']})")
    return UserResponse(
        user_id=row["user_id"],
        user_name=row["user_name"],
        email=row["email"],
        role=row["role"],
    )
