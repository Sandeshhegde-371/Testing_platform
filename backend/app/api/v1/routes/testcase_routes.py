"""
app/api/v1/routes/testcase_routes.py

Route handlers for test case CRUD, review, and approval lifecycle.

Pipeline steps: Step 5 (Review) → Step 6 (Approval)

Endpoints:
    GET    /api/v1/testcases/           → Paginated list of test cases
    POST   /api/v1/testcases/           → Create a test case manually
    GET    /api/v1/testcases/{id}       → Get a single test case
    PATCH  /api/v1/testcases/{id}       → Edit test case content
    DELETE /api/v1/testcases/{id}       → Delete a test case
    PATCH  /api/v1/testcases/{id}/status → Approve or reject
    POST   /api/v1/testcases/{id}/regenerate → Re-trigger AI for one test case
"""

from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("/", summary="List all test cases")
async def list_test_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    type: str = Query(None),
    search: str = Query(None),
):
    """
    Return a paginated, filterable list of test cases.

    Query params:
        page       : Page number (1-indexed).
        page_size  : Results per page (max 100).
        status     : Filter by status (draft | pending | approved | rejected).
        type       : Filter by test type (UI | API | Regression).
        search     : Full-text search on title and description.

    Returns:
        TestCaseListResponse: Paginated list with metadata.
    """
    pass


@router.post("/", summary="Create a test case manually", status_code=201)
async def create_test_case():
    """
    Create a new test case manually (not AI-generated).
    Useful for importing existing test cases.
    """
    pass


@router.get("/{test_case_id}", summary="Get a single test case")
async def get_test_case(test_case_id: str):
    """
    Retrieve the full detail of a single test case including BDD and Selenium code.

    Raises:
        HTTPException 404: If the test case does not exist.
    """
    pass


@router.patch("/{test_case_id}", summary="Update test case content")
async def update_test_case(test_case_id: str):
    """
    Update test case title, description, BDD content, Selenium code, or tags.
    Partial updates only – omitted fields remain unchanged.
    """
    pass


@router.delete("/{test_case_id}", summary="Delete a test case", status_code=204)
async def delete_test_case(test_case_id: str):
    """
    Hard-delete a test case. This also removes any Zephyr sync record.

    Raises:
        HTTPException 404: If not found.
        HTTPException 409: If the test case is part of an active execution.
    """
    pass


@router.patch("/{test_case_id}/status", summary="Approve or reject a test case")
async def update_test_case_status(test_case_id: str):
    """
    Transition the test case lifecycle status.

    Valid transitions:
        pending → approved
        pending → rejected
        rejected → pending  (re-review)

    Raises:
        HTTPException 409: If transition is not allowed from the current state.
    """
    pass


@router.post("/{test_case_id}/regenerate", summary="Re-trigger AI generation for one test case")
async def regenerate_test_case(test_case_id: str):
    """
    Submit a single test case for AI re-generation.
    Useful when the initial output is unsatisfactory or the prompt has changed.
    """
    pass
