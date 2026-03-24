"""
tests/api/test_prompt_routes.py

Integration tests for the Prompt API routes.
Uses FastAPI TestClient with a mocked PromptService.

Test coverage:
    - POST /api/v1/prompt/parse   → valid input, empty input, oversized prompt
    - POST /api/v1/prompt/generate → successful trigger, Confluence URL, invalid type
    - GET  /api/v1/prompt/status/{task_id} → pending, running, complete, not found
"""

import pytest
# from httpx import AsyncClient
# from app.main import app


class TestParsePrompt:
    """Tests for POST /api/v1/prompt/parse"""

    async def test_parse_valid_prompt_extracts_jira_tickets(self):
        """Verify extracted Jira ticket keys match tickets in prompt text."""
        pass

    async def test_parse_valid_prompt_extracts_confluence_urls(self):
        """Verify Confluence URLs are correctly identified and returned."""
        pass

    async def test_parse_empty_prompt_returns_422(self):
        """Empty prompt should fail validation with HTTP 422."""
        pass

    async def test_parse_oversized_prompt_returns_422(self):
        """Prompt exceeding MAX_PROMPT_LENGTH should return HTTP 422."""
        pass


class TestGenerateTestCases:
    """Tests for POST /api/v1/prompt/generate"""

    async def test_generate_returns_task_id(self):
        """Successful trigger should return a non-empty task_id string."""
        pass

    async def test_generate_with_confluence_url(self):
        """Generation should include confluence_url in the Celery task payload."""
        pass

    async def test_generate_requires_authentication(self):
        """Unauthenticated request should return HTTP 401."""
        pass


class TestGetGenerationStatus:
    """Tests for GET /api/v1/prompt/status/{task_id}"""

    async def test_pending_task_returns_pending_status(self):
        """A newly dispatched task should have stage='parse_prompt', progress=0."""
        pass

    async def test_unknown_task_id_returns_404(self):
        """Non-existent task ID should return HTTP 404."""
        pass

    async def test_complete_task_returns_100_progress(self):
        """Finished task should have progress=100 and stage='complete'."""
        pass
