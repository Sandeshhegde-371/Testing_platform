"""
app/integrations/harness_client.py

HTTP client for the Harness CI/CD REST API.

Responsibilities:
    - Trigger pipeline runs with test case payload inputs
    - Poll execution status and stream logs
    - Cancel running pipelines
    - Fetch post-execution artifacts and test reports

Usage:
    client = HarnessClient()
    run = await client.trigger_pipeline(pipeline_id="...", inputs={...})
"""


class HarnessClient:
    """
    Async HTTP client for the Harness Platform API.
    Authenticated via API key from settings.
    """

    def __init__(self):
        """Initialise with base_url, api_key, account_id, org_id, project_id from settings."""
        pass

    async def trigger_pipeline(self, pipeline_id: str, inputs: dict) -> dict:
        """
        Trigger a Harness pipeline execution.

        Args:
            pipeline_id : Harness pipeline identifier.
            inputs      : Runtime input set (test case IDs, environment, etc.).

        Returns:
            dict: {run_id, execution_url, status}
        """
        pass

    async def get_execution_status(self, run_id: str) -> dict:
        """
        Poll the current status of a pipeline execution.

        Args:
            run_id: Harness execution run ID.

        Returns:
            dict: {status, stage_executions, started_at, ended_at}
        """
        pass

    async def get_execution_logs(self, run_id: str, stage_id: str = None) -> list:
        """
        Fetch log output for a pipeline run or a specific stage.

        Args:
            run_id   : Harness execution run ID.
            stage_id : Optional stage filter.

        Returns:
            list[dict]: [{timestamp, level, message}]
        """
        pass

    async def cancel_pipeline(self, run_id: str) -> bool:
        """
        Send a cancellation request for a running pipeline.

        Returns:
            bool: True if cancellation was accepted.
        """
        pass

    async def get_test_report(self, run_id: str) -> dict:
        """
        Fetch the test report artifact from a completed pipeline run.
        Used to map Harness test results back to individual test case IDs.

        Returns:
            dict: {total, passed, failed, test_results: [...]}
        """
        pass
