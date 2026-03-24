"""
app/api/v1/api_router.py

Central API router for version 1.
Aggregates all route modules under the /api/v1 prefix.

To add a new route group:
    1. Create the route file in app/api/v1/routes/
    2. Import the router here
    3. Call api_router.include_router(...)
"""

from fastapi import APIRouter

# from app.api.v1.routes.prompt_routes import router as prompt_router
# from app.api.v1.routes.testcase_routes import router as testcase_router
# from app.api.v1.routes.zephyr_routes import router as zephyr_router
# from app.api.v1.routes.execution_routes import router as execution_router
# from app.api.v1.routes.health_routes import router as health_router

api_router = APIRouter()

# ── Register sub-routers ───────────────────────────────────────────────────────
# api_router.include_router(health_router,     prefix="/health",    tags=["Health"])
# api_router.include_router(prompt_router,     prefix="/prompt",    tags=["Prompt"])
# api_router.include_router(testcase_router,   prefix="/testcases", tags=["Test Cases"])
# api_router.include_router(zephyr_router,     prefix="/zephyr",    tags=["Zephyr"])
# api_router.include_router(execution_router,  prefix="/execution", tags=["Execution"])
