"""
app/api/v1/routes/execution_routes.py

Route handlers for triggering Harness pipeline executions and fetching results.

Pipeline steps: Step 7 (Execute via Harness) → Step 8 (Fetch Results)

Endpoints:
    POST /api/v1/execution/run              → Trigger a new pipeline run
    GET  /api/v1/execution/{id}/status      → Poll live execution status + logs
    GET  /api/v1/execution/{id}/results     → Get final results + AI insights
    POST /api/v1/execution/{id}/cancel      → Cancel a running execution
    GET  /api/v1/execution/                 → List past executions
"""

from fastapi import APIRouter, Query

router = APIRouter()


@router.post("/run", summary="Trigger a Harness pipeline execution", status_code=202)
async def run_execution():
    """
    Trigger an asynchronous Harness pipeline run for the given test cases.

    Steps:
        1. Validate test_case_ids exist and are approved.
        2. Create an Execution DB record with status=PENDING.
        3. Dispatch a Celery task (execution_tasks.run_harness_pipeline).
        4. Return the execution_id and Celery task_id for polling.

    Returns:
        ExecutionResponse: execution_id, task_id, status=PENDING.
    """
    pass


@router.get("/{execution_id}/status", summary="Poll live execution status")
async def get_execution_status(execution_id: str):
    """
    Return the live status of an execution including streaming log entries.

    Used by the Execution page to auto-refresh status and append log lines.

    Returns:
        ExecutionStatusResponse: status, progress, and accumulated logs.
    """
    pass


@router.get("/{execution_id}/results", summary="Get full execution results with AI insights")
async def get_execution_results(execution_id: str):
    """
    Return the complete results of a finished execution, including:
        - Per-test-case pass/fail status and duration
        - Execution logs
        - Links to screenshots and artifacts
        - AI-generated root cause analysis for failed tests

    Raises:
        HTTPException 404: Execution not found.
        HTTPException 409: Execution not yet complete.

    Returns:
        ExecutionResultsResponse
    """
    pass


@router.post("/{execution_id}/cancel", summary="Cancel a running execution")
async def cancel_execution(execution_id: str):
    """
    Request cancellation of an in-progress Harness pipeline run.

    Steps:
        1. Call harness_client.cancel_run(harness_run_id).
        2. Update Execution status → CANCELLED.
        3. Revoke the associated Celery task.
    """
    pass


@router.get("/", summary="List past executions")
async def list_executions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """
    Return a paginated history of all past and current executions.
    Most recent executions returned first.
    """
    pass
