"""
app/models/zephyr.py

SQLAlchemy ORM model for the ZephyrSync entity.

Tracks the synchronisation state of each test case with Zephyr Scale,
including the assigned Zephyr test case ID, project key, and sync timestamp.
Allows auditing of repeated sync attempts.
"""

from sqlalchemy import Column, String, Enum as SAEnum, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
# from app.core.database import Base
# from app.core.constants import SyncStatus


class ZephyrSync:  # (Base):
    """
    Tracks the sync state between a TestCase and Zephyr Scale.

    One ZephyrSync record per (test_case_id, zephyr_project_key) pair.

    Columns:
        id               : UUID primary key
        test_case_id     : FK → TestCase being synced
        zephyr_id        : Zephyr test case ID returned after successful push
        project_key      : Zephyr project key (e.g. "ESHOP")
        sync_status      : SyncStatus enum
        error_message    : Populated if sync failed (for debugging)
        synced_at        : Timestamp of last successful sync
        created_at       : Record creation timestamp

    Relationships:
        test_case        : The TestCase this sync record belongs to
    """

    __tablename__ = "zephyr_syncs"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # test_case_id = Column(UUID(as_uuid=True), ForeignKey("test_cases.id"), nullable=False)
    # zephyr_id = Column(String(128), nullable=True)
    # project_key = Column(String(64), nullable=False)
    # sync_status = Column(SAEnum(SyncStatus), default=SyncStatus.NOT_SYNCED)
    # error_message = Column(Text, nullable=True)
    # synced_at = Column(DateTime(timezone=True), nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        pass
