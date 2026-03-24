#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/worker.sh
# Start a Celery worker for async task processing.
# Usage: ./scripts/worker.sh [--concurrency N] [--queues generation,zephyr]
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

APP_MODULE="app.tasks.celery_app"
CONCURRENCY="${CONCURRENCY:-4}"
QUEUES="${QUEUES:-generation,zephyr,execution,default}"
LOG_LEVEL="${LOG_LEVEL:-info}"

echo "⚙️  Starting Celery worker (queues: ${QUEUES}, concurrency: ${CONCURRENCY})..."

exec celery -A "${APP_MODULE}.celery" worker \
    --loglevel="${LOG_LEVEL}" \
    --concurrency="${CONCURRENCY}" \
    --queues="${QUEUES}" \
    "$@"
