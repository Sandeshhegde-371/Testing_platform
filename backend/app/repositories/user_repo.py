"""
app/repositories/user_repo.py

Data access layer for the User entity.

Handles all DB operations for user management, authentication lookup,
and role-based queries.
"""

from typing import Optional


class UserRepository:
    """Async CRUD operations for the users table."""

    def __init__(self, session):
        """
        Args:
            session: SQLAlchemy AsyncSession instance.
        """
        pass

    async def create(self, data: dict):
        """
        Create a new user record.

        Args:
            data: {email, hashed_pw, full_name, role}

        Returns:
            User: Created ORM instance with generated UUID.
        """
        pass

    async def get_by_id(self, user_id: str):
        """
        Fetch user by primary key.

        Returns:
            User | None
        """
        pass

    async def get_by_email(self, email: str):
        """
        Fetch user by email address (used during login authentication).

        Returns:
            User | None
        """
        pass

    async def update(self, user_id: str, patch: dict):
        """
        Partially update user profile fields.

        Args:
            user_id : Target user UUID.
            patch   : Dict of {column: value} pairs to update.
        """
        pass

    async def set_active(self, user_id: str, is_active: bool):
        """
        Activate or deactivate a user account.

        Args:
            is_active: False = soft-delete (user cannot log in).
        """
        pass

    async def list(self, page: int = 1, page_size: int = 20) -> tuple:
        """
        Return paginated list of all users (admin-only endpoint).

        Returns:
            tuple: (List[User], total_count)
        """
        pass
