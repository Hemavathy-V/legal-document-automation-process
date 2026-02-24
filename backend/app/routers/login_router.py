"""
Login feature: login and register endpoints.
Routes: POST /api/login, POST /api/register
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from backend.app.auth.auth import create_access_token, get_password_hash, verify_password
from backend.app.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from backend.app.database.db_connection import get_connection
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["login"])


@router.options("/login")
def login_options():
    """CORS preflight for POST /api/login."""
    logger.debug("Login CORS preflight request")
    return {}


def _get_user_by_email(email: str) -> Optional[dict]:
    logger.debug(f"Fetching user from database: {email}")
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
        result = cursor.fetchone()
        if result:
            logger.debug(f"User found: {email} (ID: {result['user_id']})")
        else:
            logger.warning(f"User not found: {email}")
        return result
    finally:
        cursor.close()
        conn.close()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """
    Login with email and password. Returns JWT and user info.
    """
    logger.info(f"Login attempt for email: {request.email}")
    user_row = _get_user_by_email(request.email)
    if not user_row or not user_row.get("password"):
        logger.warning(f"Login failed - invalid credentials for: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(request.password, user_row["password"]):
        logger.warning(f"Login failed - password mismatch for: {request.email}")
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
    logger.info(f"User logged in successfully: {user.user_name} (ID: {user.user_id})")
    return TokenResponse(access_token=access_token, user=user)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    """
    Register a new user with password and role.
    """
    logger.info(f"Registration attempt for email: {request.email}, username: {request.user_name}")
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT user_id FROM users WHERE email = %s", (request.email,))
        if cursor.fetchone():
            logger.warning(f"Registration failed - email already registered: {request.email}")
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
            logger.warning(f"Registration failed - invalid role: {request.role}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            )

        logger.debug(f"Inserting new user: {request.user_name}")
        hashed_password = get_password_hash(request.password)
        cursor.execute(
            """
            INSERT INTO users (user_name, role_id, email, password)
            VALUES (%s, %s, %s, %s)
            """,
            (request.user_name, role_row["lookup_id"], request.email, hashed_password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        logger.info(f"User registered successfully: {request.user_name} (ID: {user_id}, Email: {request.email})")
        return UserResponse(
            user_id=user_id,
            user_name=request.user_name,
            email=request.email,
            role=request.role,
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()
