"""
app/core/security.py

Authentication and authorisation utilities.

Responsibilities:
    - JWT token creation (access + refresh)
    - JWT token decoding and validation
    - Password hashing and verification (bcrypt)
    - Dependency injection helpers for FastAPI route protection

Usage:
    from app.core.security import create_access_token, get_current_user
"""

from datetime import datetime, timedelta
from typing import Optional


# ─── Password Utilities ───────────────────────────────────────────────────────

class PasswordHasher:
    """
    Bcrypt-based password hashing wrapper.

    Methods:
        hash(plain_password)   → hashed string
        verify(plain, hashed)  → bool
    """

    def hash(self, plain_password: str) -> str:
        """Hash a plain-text password using bcrypt."""
        pass

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against its bcrypt hash."""
        pass


# ─── JWT Token Utilities ──────────────────────────────────────────────────────

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: The token subject (typically user ID or email).
        expires_delta: Optional custom expiry. Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: Encoded JWT string.
    """
    pass


def create_refresh_token(subject: str) -> str:
    """
    Create a signed JWT refresh token with longer expiry.

    Args:
        subject: The token subject.

    Returns:
        str: Encoded JWT refresh token.
    """
    pass


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: The encoded JWT string.

    Returns:
        dict: Decoded payload.

    Raises:
        HTTPException 401: If token is expired or invalid.
    """
    pass


# ─── FastAPI Dependency Helpers ───────────────────────────────────────────────

async def get_current_user(token: str):
    """
    FastAPI dependency: extract and return the current authenticated user.

    Args:
        token: Bearer token from the Authorization header (injected by FastAPI).

    Returns:
        User: The authenticated user model instance.

    Raises:
        HTTPException 401: If token is invalid or user not found.

    Usage in routes:
        @router.get("/me")
        async def me(user = Depends(get_current_user)):
            ...
    """
    pass


async def get_current_admin_user(current_user=None):
    """
    FastAPI dependency: ensure current user has admin role.

    Raises:
        HTTPException 403: If user is not an admin.
    """
    pass


# ─── Module-level singleton ───────────────────────────────────────────────────

password_hasher = PasswordHasher()
