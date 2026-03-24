"""
app/schemas/testcase_schema.py

Pydantic request and response schemas for the TestCase API.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# ─── Shared base ──────────────────────────────────────────────────────────────

class TestCaseBase(BaseModel):
    """Fields shared by create, update, and response schemas."""
    title: str
    description: Optional[str] = None
    type: str = "UI"
    tags: List[str] = []


# ─── Request Schemas ──────────────────────────────────────────────────────────

class TestCaseCreateRequest(TestCaseBase):
    """
    Payload for manually creating a test case (not AI-generated).
    Typically used in tests or admin scenarios.
    """
    bdd_content: Optional[str] = None
    selenium_code: Optional[str] = None


class TestCaseUpdateRequest(BaseModel):
    """
    Payload for PATCH /api/v1/testcases/{id}
    All fields optional – only provided fields are updated.

    Fields:
        title           : Update test case title.
        description     : Update description.
        bdd_content     : Update BDD scenario (e.g. after manual edit in UI).
        selenium_code   : Update Selenium code.
        tags            : Replace tag list.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    bdd_content: Optional[str] = None
    selenium_code: Optional[str] = None
    tags: Optional[List[str]] = None


class TestCaseStatusUpdateRequest(BaseModel):
    """
    Payload for PATCH /api/v1/testcases/{id}/status
    Used by the Review/Approval page to approve or reject a test case.

    Fields:
        status  : New status (approved | rejected | pending)
        reason  : Optional reason for rejection (stored for audit)
    """
    status: str
    reason: Optional[str] = None


# ─── Response Schemas ─────────────────────────────────────────────────────────

class TestCaseResponse(TestCaseBase):
    """
    Full test case response returned by GET /api/v1/testcases/{id}.
    Includes computed fields like sync_status and zephyr_id.
    """
    id: str
    status: str
    bdd_content: Optional[str] = None
    selenium_code: Optional[str] = None
    zephyr_id: Optional[str] = None
    sync_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TestCaseListResponse(BaseModel):
    """Paginated list response for GET /api/v1/testcases/"""
    items: List[TestCaseResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
