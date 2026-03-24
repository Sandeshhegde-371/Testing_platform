"""
app/schemas/prompt_schema.py

Pydantic request and response schemas for the Prompt API.

These schemas validate incoming requests and shape outgoing responses.
They are intentionally decoupled from ORM models so the API contract
can evolve independently of the database schema.
"""

from typing import Optional, List
from pydantic import BaseModel, HttpUrl, field_validator
# from app.core.constants import TestCaseType


# ─── Request Schemas ──────────────────────────────────────────────────────────

class PromptGenerateRequest(BaseModel):
    """
    Payload for POST /api/v1/prompt/generate

    Fields:
        prompt_text     : Free-text description of the feature / requirement.
        confluence_url  : Optional URL to a Confluence page to scrape.
        jira_ticket     : Optional Jira ticket key (e.g. "ESHOP-4521").
        test_type       : Desired test category (UI | API | Regression).
        generate_bdd    : Whether to generate Gherkin BDD scenarios.
        generate_selenium : Whether to generate Selenium Java code.
    """
    prompt_text: str
    confluence_url: Optional[HttpUrl] = None
    jira_ticket: Optional[str] = None
    test_type: str = "UI"
    generate_bdd: bool = True
    generate_selenium: bool = True

    @field_validator("prompt_text")
    @classmethod
    def validate_prompt_length(cls, v: str) -> str:
        """Ensure prompt is not empty and does not exceed the maximum length."""
        pass

    @field_validator("jira_ticket")
    @classmethod
    def validate_jira_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate Jira ticket format: PROJECT-NNNN."""
        pass


class ParsedInputResponse(BaseModel):
    """
    Response from POST /api/v1/prompt/parse – parsed input preview.

    Fields:
        confluence_links : Detected Confluence URLs.
        jira_tickets     : Detected Jira ticket keys.
        prompt_summary   : Short AI-generated summary of the prompt.
    """
    confluence_links: List[str] = []
    jira_tickets: List[str] = []
    prompt_summary: Optional[str] = None


class GenerationStatusResponse(BaseModel):
    """
    Response for generation task status polling.

    Fields:
        task_id   : Celery task ID for status polling.
        stage     : Current GenerationStage.
        progress  : 0–100 percentage.
        message   : Human-readable status message.
    """
    task_id: str
    stage: str
    progress: int = 0
    message: str = ""
