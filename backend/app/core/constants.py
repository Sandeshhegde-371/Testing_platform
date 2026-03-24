"""
app/core/constants.py

Application-wide constant values and enumerations.

Keep business constants here (status codes, default values, limits) to avoid
magic strings scattered through the codebase.
"""

from enum import Enum


# ─── Test Case Constants ──────────────────────────────────────────────────────

class TestCaseStatus(str, Enum):
    """
    Lifecycle status of a test case.

    Transitions:
        DRAFT → PENDING → APPROVED → (ZEPHYR_SYNCED)
                        ↘ REJECTED
    """
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class TestCaseType(str, Enum):
    """Category of the test case, determines generation strategy."""
    UI = "UI"
    API = "API"
    REGRESSION = "Regression"


# ─── Execution Constants ──────────────────────────────────────────────────────

class ExecutionStatus(str, Enum):
    """
    Status of a Harness pipeline execution run.

    Transitions:
        PENDING → RUNNING → PASSED
                          ↘ FAILED
        Any state → CANCELLED
    """
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ─── Zephyr Sync Constants ────────────────────────────────────────────────────

class SyncStatus(str, Enum):
    """Synchronisation status of a test case with Zephyr Scale."""
    NOT_SYNCED = "not_synced"
    SYNCING = "syncing"
    SYNCED = "synced"
    FAILED = "failed"


# ─── User / Role Constants ────────────────────────────────────────────────────

class UserRole(str, Enum):
    """Role-based access control roles."""
    ADMIN = "admin"
    TESTER = "tester"
    VIEWER = "viewer"


# ─── AI Generation Constants ──────────────────────────────────────────────────

class GenerationStage(str, Enum):
    """
    Stages of the AI generation pipeline, used for progress tracking
    and Celery task chaining.
    """
    PARSE_PROMPT = "parse_prompt"
    FETCH_CONFLUENCE = "fetch_confluence"
    FETCH_JIRA = "fetch_jira"
    GENERATE_TESTCASES = "generate_testcases"
    GENERATE_BDD = "generate_bdd"
    GENERATE_SELENIUM = "generate_selenium"
    COMPLETE = "complete"
    FAILED = "failed"


# ─── Limits & Defaults ────────────────────────────────────────────────────────

MAX_PROMPT_LENGTH: int = 10_000            # Characters
MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
MAX_TESTCASES_PER_GENERATION: int = 50
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100

API_TIMEOUT_SECONDS: int = 30              # External API calls
GENERATION_TIMEOUT_SECONDS: int = 300      # AI generation tasks

# ─── Queue Names ──────────────────────────────────────────────────────────────

QUEUE_GENERATION = "generation"
QUEUE_ZEPHYR = "zephyr"
QUEUE_EXECUTION = "execution"
QUEUE_DEFAULT = "default"
