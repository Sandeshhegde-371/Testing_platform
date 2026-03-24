"""
app/models/execution.py

SQLAlchemy ORM model for the Execution entity.

An Execution represents a single Harness pipeline run triggered for one or more
test cases. It tracks the runtime status, logs, and results.
"""

from sqlalchemy import Column, String, Text, Enum as SAEnum, DateTime, Integer, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
# from app.core.database import Base
# from app.core.constants import ExecutionStatus


class Execution:  # (Base):
    """
    Represents a Harness pipeline execution run.

    Columns:
        id                 : UUID primary key
        harness_run_id     : Harness-provided execution ID (for status polling)
        pipeline_id        : Harness pipeline identifier
        environment        : Target environment (staging | qa | production)
        status             : ExecutionStatus enum
        test_case_ids      : Array of TestCase UUIDs included in this run
        total_tests        : Count of test cases executed
        passed_count       : Count of passed test cases
        failed_count       : Count of failed test cases
        pass_rate          : Percentage (0.0 – 100.0)
        duration_seconds   : Wall-clock execution time
        logs               : JSONB array of log entries [{timestamp, level, message}]
        results            : JSONB array of per-test results
        triggered_by_id    : FK → User who triggered execution
        started_at         : When execution started
        completed_at       : When execution finished (null if still running)

    Relationships:
        triggered_by_user  : User who triggered this run
    """

    __tablename__ = "executions"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # harness_run_id = Column(String(255), nullable=True, index=True)
    # pipeline_id = Column(String(255), nullable=False)
    # environment = Column(String(64), default="staging")
    # status = Column(SAEnum(ExecutionStatus), default=ExecutionStatus.PENDING)
    # test_case_ids = Column(ARRAY(String), default=list)
    # total_tests = Column(Integer, default=0)
    # passed_count = Column(Integer, default=0)
    # failed_count = Column(Integer, default=0)
    # pass_rate = Column(Float, default=0.0)
    # duration_seconds = Column(Float, nullable=True)
    # logs = Column(JSON, default=list)
    # results = Column(JSON, default=list)
    # triggered_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    # started_at = Column(DateTime(timezone=True), nullable=True)
    # completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        pass
