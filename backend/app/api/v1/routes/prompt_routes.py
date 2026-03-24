"""
app/api/v1/routes/prompt_routes.py

Route handlers for prompt ingestion and AI generation triggering.

Pipeline step: Step 1 (Prompt Input) → Step 2 (Parse) → Step 3 (Fetch) → Step 4 (Generate)

Endpoints:
    POST /api/v1/prompt/parse      → Parse and preview input (sync, fast)
    POST /api/v1/prompt/generate   → Trigger async AI generation via Celery
    GET  /api/v1/prompt/status/{task_id}  → Poll generation task status
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form
# from app.schemas.prompt_schema import PromptGenerateRequest, ParsedInputResponse, GenerationStatusResponse
# from app.services.prompt_service import PromptService
# from app.core.security import get_current_user

router = APIRouter()


@router.post("/parse", summary="Parse and preview prompt input")
async def parse_prompt(
    # request: PromptGenerateRequest,
    # current_user=Depends(get_current_user),
):
    """
    Synchronously parse the submitted prompt and return a preview.

    Detects:
        - Confluence page URLs
        - Jira ticket keys (e.g. ESHOP-4521)
        - Free-text requirement summary

    Returns:
        ParsedInputResponse: Detected links, tickets, and prompt summary.
    """
    pass


@router.post("/generate", summary="Trigger AI test case generation")
async def generate_test_cases(
    # request: PromptGenerateRequest,
    # current_user=Depends(get_current_user),
    # service: PromptService = Depends(),
):
    """
    Trigger asynchronous AI test case generation via Celery.

    Steps orchestrated:
        1. Parse prompt
        2. Fetch Confluence page content (if URL provided)
        3. Fetch Jira ticket description (if ticket key provided)
        4. Send combined context to LLM (BDD generation)
        5. Send context to LLM (Selenium code generation)
        6. Persist generated test cases to DB

    Returns:
        GenerationStatusResponse: Celery task ID and initial status.
    """
    pass


@router.get("/status/{task_id}", summary="Poll generation task status")
async def get_generation_status(
    task_id: str,
    # current_user=Depends(get_current_user),
):
    """
    Poll the status of an ongoing or completed AI generation task.

    Args:
        task_id: Celery task ID returned by /generate.

    Returns:
        GenerationStatusResponse: Current stage, progress (0–100), and log message.
    """
    pass
