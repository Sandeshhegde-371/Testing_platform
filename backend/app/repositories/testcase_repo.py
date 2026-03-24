"""
app/repositories/testcase_repo.py

Data access layer for the TestCase entity.

All database queries for TestCase are centralised here.
Services call this repository; they never construct SQLAlchemy queries directly.
This enables swapping the ORM or database without touching business logic.

Usage:
    repo = TestCaseRepository(db_session)
    cases = await repo.list(page=1, page_size=20, status="approved")
"""

from typing import List, Optional


class TestCaseRepository:
    """
    Provides async CRUD operations for the test_cases table.
    Accepts an AsyncSession in the constructor (injected via FastAPI DI).
    """

    def __init__(self, session):
        """
        Args:
            session: SQLAlchemy AsyncSession instance.
        """
        pass

    async def create(self, data: dict):
        """
        Insert a new TestCase row.

        Args:
            data: Dict of column values (mapped to TestCase model).

        Returns:
            TestCase: Newly persisted ORM instance with generated ID.
        """
        pass

    async def get_by_id(self, test_case_id: str):
        """
        Fetch a single TestCase by primary key.

        Returns:
            TestCase | None
        """
        pass

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        test_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple:
        """
        Return paginated test cases with optional filters.

        Args:
            page       : 1-indexed page number.
            page_size  : Number of results per page.
            status     : Filter by TestCaseStatus value.
            test_type  : Filter by TestCaseType value.
            search     : Partial match on title / description (ILIKE).

        Returns:
            tuple: (List[TestCase], total_count)
        """
        pass

    async def update(self, test_case_id: str, patch: dict):
        """
        Apply a partial update to existing columns.

        Args:
            test_case_id : Target row ID.
            patch        : Dict of {column: new_value} pairs.

        Returns:
            TestCase: Updated instance.
        """
        pass

    async def delete(self, test_case_id: str) -> bool:
        """
        Hard-delete a TestCase row.

        Returns:
            bool: True if a row was deleted, False if not found.
        """
        pass

    async def find_by_title_similarity(self, title: str, threshold: float = 0.8) -> List:
        """
        Find test cases with similar titles (for duplicate detection).
        Uses PostgreSQL similarity() or trigram index.

        Returns:
            List[TestCase]: Potential duplicates ordered by similarity.
        """
        pass

    async def bulk_update_status(self, test_case_ids: List[str], status: str) -> int:
        """
        Update status for multiple test cases in a single query.

        Returns:
            int: Number of rows updated.
        """
        pass
