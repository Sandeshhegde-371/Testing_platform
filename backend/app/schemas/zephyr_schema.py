"""
app/schemas/zephyr_schema.py

Pydantic schemas for the Zephyr Integration API.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# ─── Request Schemas ──────────────────────────────────────────────────────────

class ZephyrPushRequest(BaseModel):
    """
    Payload for POST /api/v1/zephyr/push

    Fields:
        test_case_ids  : List of TestCase IDs to push to Zephyr.
        project_key    : Zephyr project key (defaults to settings.ZEPHYR_PROJECT_KEY).
        folder_name    : Optional Zephyr folder to organise tests into.
    """
    test_case_ids: List[str]
    project_key: Optional[str] = None
    folder_name: Optional[str] = None


# ─── Response Schemas ─────────────────────────────────────────────────────────

class ZephyrConnectionStatus(BaseModel):
    """
    Response for GET /api/v1/zephyr/status
    Checks that the Zephyr API token is valid and the project exists.
    """
    connected: bool
    project_key: str
    base_url: str
    last_sync: Optional[datetime] = None
    error: Optional[str] = None


class ZephyrSyncResult(BaseModel):
    """Result for a single test case sync operation."""
    test_case_id: str
    test_case_title: str
    zephyr_id: Optional[str] = None
    sync_status: str
    error: Optional[str] = None


class ZephyrPushResponse(BaseModel):
    """
    Response for POST /api/v1/zephyr/push
    Summary of the bulk push operation.
    """
    total_requested: int
    pushed_count: int
    failed_count: int
    results: List[ZephyrSyncResult]


class ZephyrTestCaseResponse(BaseModel):
    """
    A test case as it appears in the Zephyr sync table.
    Used by GET /api/v1/zephyr/synced
    """
    test_case_id: str
    title: str
    zephyr_id: Optional[str] = None
    sync_status: str
    synced_at: Optional[datetime] = None
    project_key: str

    model_config = {"from_attributes": True}
