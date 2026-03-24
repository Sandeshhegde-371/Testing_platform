"""
app/api/v1/routes/health_routes.py

Health check endpoints.
Used by load balancers, container orchestrators (k8s liveness/readiness probes),
and uptime monitors.

Endpoints:
    GET /api/v1/health/           → liveness probe (is the process alive?)
    GET /api/v1/health/ready      → readiness probe (can it serve traffic?)
    GET /api/v1/health/detailed   → deep health check including DB and Redis
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Liveness probe")
async def liveness():
    """
    Liveness probe: returns 200 OK if the process is running.
    Does not check external dependencies.
    """
    pass


@router.get("/ready", summary="Readiness probe")
async def readiness():
    """
    Readiness probe: returns 200 OK only if the app can serve traffic.
    Checks that the DB connection pool is available.
    """
    pass


@router.get("/detailed", summary="Detailed health check")
async def detailed_health():
    """
    Deep health check.

    Checks:
        - Database connectivity (simple SELECT 1 query)
        - Redis ping
        - Celery worker availability (inspect active queues)

    Returns:
        dict: Status of each dependency (healthy | degraded | unhealthy).
    """
    pass
