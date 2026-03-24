#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# scripts/migrate.sh
# Run Alembic database migrations.
# Usage: ./scripts/migrate.sh              → upgrade to head
#        ./scripts/migrate.sh revision     → autogenerate a new revision
#        ./scripts/migrate.sh downgrade -1 → roll back one revision
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

ACTION="${1:-upgrade head}"

echo "🗄️  Running Alembic migration: ${ACTION}..."
alembic ${ACTION}
echo "✅ Migration complete."
