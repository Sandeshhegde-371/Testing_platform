"""
app/models/user.py

SQLAlchemy ORM model for the User entity.

Represents an authenticated platform user with a role-based access level.
Related to:
    - TestCase (created_by FK)
    - Execution (triggered_by FK)
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
# from app.core.database import Base          # uncomment when wiring DB
# from app.core.constants import UserRole


class User:  # (Base):
    """
    Represents a platform user.

    Columns:
        id          : UUID primary key (auto-generated)
        email       : Unique email address (used as login identifier)
        hashed_pw   : bcrypt-hashed password (never return in API response)
        full_name   : Display name
        role        : UserRole enum (admin | tester | viewer)
        is_active   : Soft-delete flag; inactive users cannot log in
        created_at  : Timestamp of account creation
        updated_at  : Last profile update timestamp

    Relationships:
        test_cases  : TestCase objects created by this user
        executions  : Execution objects triggered by this user
    """

    __tablename__ = "users"

    # Columns (placeholders – uncomment when Base is wired)
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # email = Column(String(255), unique=True, nullable=False, index=True)
    # hashed_pw = Column(String(255), nullable=False)
    # full_name = Column(String(255), nullable=True)
    # role = Column(SAEnum(UserRole), default=UserRole.TESTER, nullable=False)
    # is_active = Column(Boolean, default=True, nullable=False)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (placeholders)
    # test_cases = relationship("TestCase", back_populates="created_by_user")
    # executions = relationship("Execution", back_populates="triggered_by_user")

    def __repr__(self) -> str:
        """Human-readable representation for debugging."""
        pass
