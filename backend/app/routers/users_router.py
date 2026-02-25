"""
Users management: list, update, and delete users.
Routes:
    GET    /api/users            (Admin only)
    PATCH  /api/users/{user_id}  (Admin only)
    DELETE /api/users/{user_id}  (Admin only)
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from mysql.connector.errors import IntegrityError

from backend.app.auth import get_password_hash
from backend.app.deps import get_current_user
from backend.app.schemas import UserResponse, UserUpdateRequest
from backend.database.db_connection import get_connection
from backend.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["users"])


def _require_admin(current_user: UserResponse) -> None:
    if current_user.role != "Admin":
        logger.warning(
            f"Unauthorised /users access by {current_user.email} (role: {current_user.role})"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )


@router.get("/users", response_model=List[UserResponse])
def list_users(current_user: UserResponse = Depends(get_current_user)):
    """List all users with their roles. Admin access only."""
    _require_admin(current_user)
    logger.info(f"Admin {current_user.email} requested user list")
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
            ORDER BY u.user_id
            """
        )
        users = cursor.fetchall()
        logger.info(f"Returning {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    body: UserUpdateRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """Update a user by ID. Admin access only."""
    _require_admin(current_user)

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, user_name, email FROM users WHERE user_id = %s",
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found.",
            )

        # Check email uniqueness when changing to a different address
        if body.email != row["email"]:
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (body.email,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        cursor.execute(
            """
            SELECT lookup_id FROM look_up
            WHERE lookup_type = 'user_role' AND lookup_value = %s
            """,
            (body.role,),
        )
        role_row = cursor.fetchone()
        if not role_row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            )

        if body.password:
            hashed = get_password_hash(body.password)
            cursor.execute(
                """
                UPDATE users
                SET user_name = %s, email = %s, password = %s, role_id = %s
                WHERE user_id = %s
                """,
                (body.user_name, body.email, hashed, role_row["lookup_id"], user_id),
            )
        else:
            cursor.execute(
                """
                UPDATE users
                SET user_name = %s, email = %s, role_id = %s
                WHERE user_id = %s
                """,
                (body.user_name, body.email, role_row["lookup_id"], user_id),
            )
        conn.commit()
        logger.info(
            f"Admin {current_user.email} updated user {user_id} ({body.user_name})"
        )
        return UserResponse(
            user_id=user_id,
            user_name=body.user_name,
            email=body.email,
            role=body.role,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: UserResponse = Depends(get_current_user)):
    """Delete a user by ID. Admin access only. Cannot delete yourself."""
    _require_admin(current_user)

    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account.",
        )

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT user_id, user_name FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found.",
            )

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        logger.info(
            f"Admin {current_user.email} deleted user {user_id} ({row['user_name']})"
        )
    except HTTPException:
        raise
    except IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot delete user '{row['user_name']}': "
                "they have contracts or other linked records. "
                "Reassign or remove those records first."
            ),
        )
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
