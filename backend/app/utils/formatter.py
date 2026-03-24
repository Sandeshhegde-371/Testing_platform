"""
app/utils/formatter.py

Output formatting utilities used across services and routes.

Provides:
    - Standardised API response wrappers
    - Test case title → Java class name conversion
    - Gherkin content prettifying
    - Duration formatting (seconds → human-readable)
    - Pagination metadata builders
"""

from typing import Any, Optional


class ResponseFormatter:
    """
    Builds consistent API response envelopes for all endpoints.

    Success format:
        { "success": true, "data": {...}, "message": "..." }

    Error format:
        { "success": false, "error": "...", "detail": {...} }
    """

    @staticmethod
    def success(data: Any, message: str = "Success") -> dict:
        """
        Wrap data in a standard success envelope.

        Args:
            data    : The response payload.
            message : Human-readable success message.

        Returns:
            dict: Standard success response.
        """
        pass

    @staticmethod
    def error(message: str, detail: Optional[Any] = None) -> dict:
        """
        Wrap an error in a standard error envelope.

        Args:
            message : Error summary.
            detail  : Optional debug detail (excluded in production).

        Returns:
            dict: Standard error response.
        """
        pass

    @staticmethod
    def paginated(items: list, total: int, page: int, page_size: int) -> dict:
        """
        Build a paginated response envelope.

        Returns:
            dict: {items, total, page, page_size, has_next, has_prev}
        """
        pass


def java_class_name(title: str) -> str:
    """
    Convert a test case title to a valid Java PascalCase class name.

    Example:
        "User Login – Happy Path" → "UserLoginHappyPath"

    Args:
        title: Raw test case title string.

    Returns:
        str: Java-safe PascalCase class name.
    """
    pass


def format_duration(seconds: float) -> str:
    """
    Convert seconds to a human-readable duration string.

    Examples:
        45.2   → "45s"
        123.0  → "2m 3s"
        3661.0 → "1h 1m 1s"
    """
    pass
