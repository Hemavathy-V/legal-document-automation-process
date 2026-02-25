from datetime import datetime, timedelta, timezone
from typing import Optional
import os

import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.app.core.logger import get_logger

logger = get_logger(__name__)


SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_TO_A_LONG_RANDOM_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash."""
    logger.debug("Verifying password")
    try:
        result = bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        result = False
    logger.debug(f"Password verification result: {result}")
    return result


def get_password_hash(password: str) -> str:
    """Hash a plain-text password with bcrypt (cost factor 12)."""
    logger.debug("Generating password hash")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    logger.debug("Password hash generated successfully")
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    logger.debug(f"Creating access token for user: {data.get('sub', 'Unknown')}")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Access token created successfully for user: {data.get('sub', 'Unknown')}")
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        logger.debug("Decoding JWT token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token decoded successfully for user: {payload.get('sub', 'Unknown')}")
        return payload
    except JWTError as exc:
        logger.error(f"Failed to decode token: {str(exc)}")
        raise ValueError("Invalid token") from exc
