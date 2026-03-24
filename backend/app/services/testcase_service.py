"""
app/services/testcase_service.py

Business logic for test case lifecycle management.

Responsibilities:
    - CRUD operations (delegates DB access to TestCaseRepository)
    - Status transition validation (enforce allowed lifecycle states)
    - Duplicate detection before persisting AI-generated test cases
    - Bulk operations (approve all, bulk delete)
    - Pagination helpers

Dependencies:
    - TestCaseRepository (app.repositories.testcase_repo)
"""

from typing import List, Optional


class TestCaseService:
    """
    Handles all business logic for the TestCase lifecycle.
    Sits between route handlers and the repository layer.
    """

    def __init__(self):
        """Initialise with TestCaseRepository dependency."""
        pass

    async def list_test_cases(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        test_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> dict:
        """
        Return a paginated, optionally-filtered list of test cases.

        Args:
            page       : 1-indexed page number.
            page_size  : Results per page.
            status     : Filter by TestCaseStatus.
            test_type  : Filter by TestCaseType.
            search     : Full-text search on title and description.

        Returns:
            dict: {items, total, page, page_size, has_next}
        """
        pass

    async def get_test_case(self, test_case_id: str):
        """
        Retrieve a single test case by ID.

        Raises:
            HTTPException 404: If not found.
        """
        pass

    async def create_test_case(self, data: dict, created_by_id: str):
        """
        Persist a new test case record.

        Args:
            data          : Validated create request dict.
            created_by_id : ID of the creating user.

        Returns:
            TestCase: Newly created ORM instance.
        """
        pass

    async def update_test_case(self, test_case_id: str, patch: dict):
        """
        Apply a partial update to an existing test case.

        Args:
            test_case_id : Target test case ID.
            patch        : Dict of fields to update (only non-None values applied).

        Returns:
            TestCase: Updated ORM instance.
        """
        pass

    async def delete_test_case(self, test_case_id: str):
        """
        Delete a test case if it is not part of an active execution.

        Raises:
            HTTPException 409: If test case is referenced by a running execution.
        """
        pass

    async def update_status(self, test_case_id: str, new_status: str, reason: Optional[str] = None):
        """
        Transition the test case to a new lifecycle status.

        Validates that the transition is allowed before applying:
            pending → approved | rejected
            rejected → pending

        Raises:
            HTTPException 409: If transition is not allowed from current status.
        """
        pass

    async def detect_duplicates(self, title: str) -> List[str]:
        """
        Check if a test case with the same or similar title already exists.

        Returns:
            List[str]: IDs of potential duplicates (empty list if none).
        """
        pass

    async def bulk_approve(self, test_case_ids: List[str]):
        """
        Approve multiple test cases in a single operation.

        Args:
            test_case_ids: List of IDs to approve.

        Returns:
            int: Count of successfully approved test cases.
        """
        pass
