"""
app/tasks/zephyr_tasks.py

Celery tasks for async Zephyr Scale synchronisation.

Running sync operations asynchronously prevents the API from timing out
on bulk pushes (Zephyr rate-limits to ~10 req/s).
"""

# from app.tasks.celery_app import celery
# from app.services.zephyr_service import ZephyrService


# @celery.task(bind=True, queue="zephyr", max_retries=5, default_retry_delay=30)
def push_to_zephyr_task(self, test_case_ids: list, project_key: str) -> dict:
    """
    Celery task: push a list of test cases to Zephyr Scale.

    Handles:
        - Per-test-case create or update logic
        - Exponential backoff on 429 Rate Limit responses
        - Partial failure: continues remaining items on individual failures
        - Updates each test case sync_status and zephyr_id in DB after each push

    Args:
        test_case_ids : List of TestCase IDs to process.
        project_key   : Zephyr project key.

    Returns:
        dict: {pushed_count, failed_count, results: [...]}
    """
    pass


# @celery.task(bind=True, queue="zephyr", max_retries=3)
def push_single_to_zephyr_task(self, test_case_id: str, project_key: str) -> dict:
    """
    Celery task: push a single test case to Zephyr.
    Used for "Re-sync" button actions in the UI.

    Returns:
        dict: ZephyrSyncResult for this test case.
    """
    pass
