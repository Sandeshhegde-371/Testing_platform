"""
app/services/execution_service.py

Business logic for triggering and monitoring Harness pipeline executions.

Responsibilities:
    - Validate test case selection before triggering
    - Create Execution DB records and dispatch Celery tasks
    - Poll Harness API for live status and log streaming
    - Persist results and trigger AI insight generation
    - Handle cancellation requests

Dependencies:
    - HarnessClient      (app.integrations.harness_client)
    - AIService          (app.services.ai_service)
    - ExecutionRepository (app.repositories.execution_repo)
"""


class ExecutionService:
    """
    Orchestrates Harness pipeline execution lifecycle:
        trigger → poll status → fetch results → generate AI insights
    """

    def __init__(self):
        """Initialise with HarnessClient, AIService, and ExecutionRepository."""
        pass

    async def trigger_execution(self, test_case_ids: list, pipeline_id: str, environment: str) -> dict:
        """
        Create an Execution record and dispatch the Celery execution task.

        Steps:
            1. Validate test_case_ids are approved.
            2. Create Execution DB record with status=PENDING.
            3. Dispatch execution_tasks.run_harness_pipeline.delay(...).
            4. Return execution_id and task_id.

        Args:
            test_case_ids : List of approved TestCase IDs.
            pipeline_id   : Harness pipeline ID.
            environment   : Target env (staging | qa | production).

        Returns:
            dict: {execution_id, task_id, status}
        """
        pass

    async def get_status(self, execution_id: str) -> dict:
        """
        Return the current status of an execution, including live logs.

        Polls the Harness API if status is RUNNING, otherwise returns DB state.

        Returns:
            dict: {execution_id, status, progress, logs}
        """
        pass

    async def get_results(self, execution_id: str) -> dict:
        """
        Return full execution results including per-test results and AI insights.

        If AI insights have not yet been generated (async), triggers generation.

        Raises:
            HTTPException 409: If execution is not yet complete.
        """
        pass

    async def cancel_execution(self, execution_id: str) -> bool:
        """
        Cancel a RUNNING execution via Harness API and update DB status.

        Returns:
            bool: True if cancellation was accepted by Harness.
        """
        pass

    async def list_executions(self, page: int = 1, page_size: int = 20) -> dict:
        """
        Return paginated execution history, most recent first.
        """
        pass
