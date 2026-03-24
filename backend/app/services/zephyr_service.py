"""
app/services/zephyr_service.py

Business logic for Zephyr Scale synchronisation.

Responsibilities:
    - Validate Zephyr API connectivity before sync attempts
    - Push approved test cases to Zephyr (single and bulk)
    - Persist returned Zephyr IDs in the DB
    - Handle partial push failures gracefully

Dependencies:
    - ZephyrClient       (app.integrations.zephyr_client)
    - TestCaseRepository (app.repositories.testcase_repo)
"""


class ZephyrService:
    """
    Orchestrates all Zephyr Scale synchronisation operations.
    Delegates HTTP calls to ZephyrClient and DB updates to repositories.
    """

    def __init__(self):
        """Initialise with ZephyrClient and TestCaseRepository dependencies."""
        pass

    async def check_connection(self) -> dict:
        """
        Verify Zephyr API connectivity and project access.

        Returns:
            dict: {connected, project_key, base_url, last_sync}
        """
        pass

    async def push_test_cases(self, test_case_ids: list, project_key: str = None) -> dict:
        """
        Push a list of approved test cases to Zephyr Scale.

        For each test case:
            - If zephyr_id exists: call update_test_case on Zephyr.
            - Otherwise: call create_test_case on Zephyr, store returned ID.

        Args:
            test_case_ids : List of TestCase IDs to sync.
            project_key   : Override project key (uses settings default if None).

        Returns:
            dict: {pushed_count, failed_count, results: [ZephyrSyncResult]}
        """
        pass

    async def push_single(self, test_case_id: str) -> dict:
        """
        Push a single test case. Used for the "Re-sync" button in the UI.

        Returns:
            dict: ZephyrSyncResult for this test case.
        """
        pass

    async def get_synced_test_cases(self) -> list:
        """
        Return all test cases with sync_status = 'synced' including their Zephyr IDs.
        """
        pass
