"""
app/core/config.py

Centralised application configuration using Pydantic Settings.
All configuration is loaded from environment variables (or .env file).
Access settings throughout the app via: from app.core.config import settings
"""

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Groups:
        - Application     : app name, env, debug flag
        - Database        : PostgreSQL connection string and pool config
        - Redis           : cache and broker URLs
        - AI / LLM        : Google Gemini API key and model params
        - Jira            : Atlassian Jira credentials
        - Confluence      : Atlassian Confluence credentials
        - Zephyr          : Zephyr Scale API credentials
        - Harness         : Harness CI/CD pipeline credentials
        - JWT Auth        : token secrets and expiry
        - CORS            : allowed frontend origins
        - Logging         : log level and format
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ───────────────────────────────────────────────────────────
    APP_NAME: str = "AI Test Automation Platform"
    APP_ENV: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    API_V1_PREFIX: str = "/api/v1"

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/testai_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── AI / LLM ──────────────────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    LLM_MODEL: str = "gemini-2.0-flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 8192
    EMBEDDING_MODEL: str = "models/text-embedding-004"

    # ── Jira ──────────────────────────────────────────────────────────────────
    JIRA_BASE_URL: str = ""
    JIRA_API_TOKEN: str = ""
    JIRA_USER_EMAIL: str = ""
    JIRA_PROJECT_KEY: str = ""

    # ── Confluence ────────────────────────────────────────────────────────────
    CONFLUENCE_BASE_URL: str = ""
    CONFLUENCE_API_TOKEN: str = ""
    CONFLUENCE_USER_EMAIL: str = ""

    # ── Zephyr Scale ──────────────────────────────────────────────────────────
    ZEPHYR_BASE_URL: str = ""
    ZEPHYR_API_TOKEN: str = ""
    ZEPHYR_PROJECT_KEY: str = ""

    # ── Harness ───────────────────────────────────────────────────────────────
    HARNESS_BASE_URL: str = ""
    HARNESS_API_KEY: str = ""
    HARNESS_ACCOUNT_ID: str = ""
    HARNESS_ORG_ID: str = ""
    HARNESS_PROJECT_ID: str = ""
    HARNESS_PIPELINE_ID: str = ""

    # ── JWT Auth ──────────────────────────────────────────────────────────────
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"


@lru_cache()
def get_settings() -> Settings:
    """
    Return a cached singleton instance of Settings.
    Uses lru_cache so the .env file is read only once.

    Usage:
        from app.core.config import settings
    """
    return Settings()


# Module-level singleton for convenient import
settings: Settings = get_settings()
