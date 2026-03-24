"""
alembic/env.py

Alembic migration environment configuration.

Supports:
    - Sync offline migrations (generates SQL scripts)
    - Async online migrations (runs against live PostgreSQL via asyncpg)
    - Auto-import of all SQLAlchemy models for autogenerate to detect changes

Usage:
    alembic upgrade head                     # Apply all pending migrations
    alembic revision --autogenerate -m "msg" # Auto-generate migration from model changes
    alembic downgrade -1                     # Roll back one revision
"""

from logging.config import fileConfig

from alembic import context

# Alembic Config object (access to alembic.ini values)
config = context.config

# ── Logging ───────────────────────────────────────────────────────────────────
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Import all models so Alembic can detect schema changes ───────────────────
# from app.models.user import User          # noqa: F401
# from app.models.testcase import TestCase  # noqa: F401
# from app.models.execution import Execution  # noqa: F401
# from app.models.zephyr import ZephyrSync  # noqa: F401
# from app.core.database import Base

# target_metadata = Base.metadata
target_metadata = None


def get_database_url() -> str:
    """
    Load DATABASE_URL from environment or alembic.ini.
    Converts async URL (asyncpg) to sync URL (psycopg2) for Alembic compatibility.
    """
    # import os
    # url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url", ""))
    # return url.replace("+asyncpg", "")  # Alembic needs sync driver
    pass


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode (no live DB connection).
    Outputs SQL to stdout or a file for review before application.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode (connects directly to DB).
    Used during normal deployment: `alembic upgrade head`
    """
    # from sqlalchemy import create_engine
    # engine = create_engine(get_database_url())
    # with engine.connect() as connection:
    #     context.configure(connection=connection, target_metadata=target_metadata)
    #     with context.begin_transaction():
    #         context.run_migrations()
    pass


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
