"""
app/utils/validators.py

Input validation helpers used across services and route handlers.

Provides standalone validation functions (not Pydantic validators)
for business-rule validation that goes beyond field-level schema checks.
"""

from typing import List, Optional


def validate_test_case_ids_exist(ids: List[str], existing_ids: List[str]) -> List[str]:
    """
    Check that all requested test case IDs exist in the database.

    Args:
        ids          : List of submitted test case IDs.
        existing_ids : List of IDs confirmed to exist in the DB.

    Returns:
        List[str]: IDs from 'ids' that are NOT in 'existing_ids' (missing).

    Usage:
        missing = validate_test_case_ids_exist(request_ids, db_ids)
        if missing:
            raise HTTPException(404, detail=f"Test cases not found: {missing}")
    """
    pass


def validate_status_transition(current: str, requested: str) -> bool:
    """
    Validate that a requested status transition is allowed.

    Allowed transitions:
        pending  → approved | rejected
        rejected → pending
        draft    → pending

    Args:
        current   : Current TestCaseStatus value.
        requested : Requested new status.

    Returns:
        bool: True if transition is allowed.
    """
    pass


def validate_prompt_text(text: str, max_length: int = 10_000) -> str:
    """
    Validate and clean a prompt text input.

    Checks:
        - Not empty after stripping whitespace
        - Does not exceed max_length

    Returns:
        str: Stripped, valid prompt text.

    Raises:
        ValueError: If validation fails.
    """
    pass


def validate_jira_ticket_format(ticket: Optional[str]) -> Optional[str]:
    """
    Validate that a Jira ticket key matches the PROJECT-NNNN format.

    Args:
        ticket: Raw Jira ticket key string.

    Returns:
        str | None: Validated ticket key (uppercased), or None if not provided.

    Raises:
        ValueError: If ticket string does not match expected format.
    """
    pass


def validate_environment(env: str) -> str:
    """
    Ensure the requested environment is in the list of allowed values.

    Allowed: staging | qa | production

    Raises:
        ValueError: If environment is not allowed.
    """
    pass
