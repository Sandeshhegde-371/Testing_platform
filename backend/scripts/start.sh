#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/start.sh
# Start the FastAPI application using Uvicorn.
# Usage: ./scripts/start.sh [--reload] [--workers N]
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

APP_MODULE="app.main:app"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
LOG_LEVEL="${LOG_LEVEL:-info}"
WORKERS="${WORKERS:-1}"

echo "🚀 Starting TestAI API server on ${HOST}:${PORT}..."

exec uvicorn "${APP_MODULE}" \
    --host "${HOST}" \
    --port "${PORT}" \
    --log-level "${LOG_LEVEL}" \
    --workers "${WORKERS}" \
    "$@"
