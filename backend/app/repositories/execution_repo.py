"""
app/repositories/execution_repo.py

Data access layer for the Execution entity.

Provides all DB queries related to pipeline execution records, including
status updates during polling and result persistence after completion.
"""

from typing import List, Optional


class ExecutionRepository:
    """Async CRUD operations for the executions table."""

    def __init__(self, session):
        """
        Args:
            session: SQLAlchemy AsyncSession instance.
        """
        pass

    async def create(self, data: dict):
        """
        Create a new Execution record (initial status=PENDING).

        Args:
            data: Dict matching Execution model columns.

        Returns:
            Execution: Newly persisted ORM instance.
        """
        pass

    async def get_by_id(self, execution_id: str):
        """
        Fetch a single Execution by ID.

        Returns:
            Execution | None
        """
        pass

    async def update_status(self, execution_id: str, status: str, extra: dict = None):
        """
        Update execution status and optionally additional fields.

        Args:
            execution_id : Target execution ID.
            status       : New ExecutionStatus value.
            extra        : Additional column updates (e.g. completed_at, pass_rate).
        """
        pass

    async def append_logs(self, execution_id: str, log_entries: List[dict]):
        """
        Append log entries to the execution's JSONB logs column.

        Used during live streaming from the Harness API.

        Args:
            log_entries: List of {timestamp, level, message} dicts.
        """
        pass

    async def save_results(self, execution_id: str, results: List[dict], summary: dict):
        """
        Persist final per-test results and summary statistics after completion.

        Args:
            results : List of per-test-case result dicts.
            summary : {total_tests, passed, failed, pass_rate, duration_seconds}
        """
        pass

    async def list(self, page: int = 1, page_size: int = 20) -> tuple:
        """
        Return paginated list of executions, most recent first.

        Returns:
            tuple: (List[Execution], total_count)
        """
        pass
