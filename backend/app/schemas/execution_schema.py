"""
app/schemas/execution_schema.py

Pydantic schemas for the Execution API.
Covers triggering runs, polling status, and retrieving results with AI insights.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# ─── Request Schemas ──────────────────────────────────────────────────────────

class ExecutionRunRequest(BaseModel):
    """
    Payload for POST /api/v1/execution/run

    Fields:
        test_case_ids : List of TestCase IDs to include in this run.
        pipeline_id   : Harness pipeline identifier (overrides default).
        environment   : Target environment (staging | qa | production).
    """
    test_case_ids: List[str]
    pipeline_id: Optional[str] = None
    environment: str = "staging"


# ─── Sub-schemas ──────────────────────────────────────────────────────────────

class LogEntry(BaseModel):
    """Single log line within an execution."""
    timestamp: str
    level: str          # info | success | error | warn | action
    message: str


class AIInsightSchema(BaseModel):
    """
    AI-generated root cause analysis for a failed test case.

    Fields:
        root_cause      : Plain-language explanation of why the test failed.
        suggested_fix   : Recommended code or configuration change.
        impacted_tests  : Other test case IDs likely affected by the same root cause.
        confidence      : 0.0–1.0 confidence score from the AI model.
    """
    root_cause: str
    suggested_fix: str
    impacted_tests: List[str] = []
    confidence: float = 0.0


class TestResultSchema(BaseModel):
    """Result of a single test case within an execution."""
    test_case_id: str
    test_case_title: str
    status: str
    duration_ms: int
    logs: List[LogEntry] = []
    screenshots: List[str] = []
    artifacts: List[str] = []
    ai_insight: Optional[AIInsightSchema] = None


# ─── Response Schemas ─────────────────────────────────────────────────────────

class ExecutionResponse(BaseModel):
    """Response for POST /api/v1/execution/run – initial trigger acknowledgement."""
    execution_id: str
    task_id: str                # Celery task ID for polling
    status: str
    message: str


class ExecutionStatusResponse(BaseModel):
    """Response for GET /api/v1/execution/{id}/status – live status polling."""
    execution_id: str
    harness_run_id: Optional[str] = None
    status: str
    progress: int = 0
    logs: List[LogEntry] = []


class ExecutionResultsResponse(BaseModel):
    """
    Full results response for GET /api/v1/execution/{id}/results
    Returned after execution completes.
    """
    execution_id: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    pass_rate: float
    duration_seconds: float
    results: List[TestResultSchema]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
