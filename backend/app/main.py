"""
app/main.py

Application entry point.
Initialises the FastAPI app, registers middleware, includes API routers,
and wires up startup / shutdown lifecycle events.

Pipeline this file enables:
  HTTP Request → Middleware → API Router → Route Handler → Service → Repository / Integration
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Internal imports (implemented later)
# from app.core.config import settings
# from app.core.logging import configure_logging
# from app.api.v1.api_router import api_router
# from app.core.database import engine, Base


# ─── Lifespan ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for application startup and shutdown events.

    Startup:
        - Configure structured logging
        - Create DB tables (dev only – use Alembic in production)
        - Warm up vector store / RAG retriever
        - Verify external service connectivity

    Shutdown:
        - Close DB connection pool
        - Flush pending Celery tasks
        - Release Redis connections
    """
    # TODO: startup logic
    yield
    # TODO: shutdown logic


# ─── App Factory ─────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="AI Test Automation Platform",
        description="AI-powered test case lifecycle management: Prompt → Generate → Review → Zephyr → Execute → Results",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    _register_middleware(app)
    _register_routers(app)

    return app


def _register_middleware(app: FastAPI) -> None:
    """
    Attach all middleware to the FastAPI application.

    Middleware registered:
        - CORS: Allow configured origins (from settings)
        - Request ID: Attach unique ID to each request for tracing
        - Timing: Log request duration
    """
    # TODO: read allowed_origins from settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],       # Replace with settings.ALLOWED_ORIGINS
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # TODO: add RequestIDMiddleware
    # TODO: add TimingMiddleware


def _register_routers(app: FastAPI) -> None:
    """
    Include all versioned API routers.

    Currently registers:
        - /api/v1  → all v1 routes (prompt, testcases, zephyr, execution, health)
    """
    # TODO: app.include_router(api_router, prefix="/api/v1")
    pass


# ─── App Instance ─────────────────────────────────────────────────────────────

app = create_app()
