# Backend Documentation — AI Test Automation Platform

Complete reference for every folder, file, and Python module in the backend scaffold.

---

## Architecture Overview

The backend follows **Clean / Layered Architecture**. Each layer has a single responsibility and can be replaced without touching other layers.

```
HTTP Request
    │
    ▼
┌─────────────────────────────────┐
│  API Layer  (routes/)           │  Validates input, calls Services
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  Service Layer  (services/)     │  Business logic, orchestration
└──────┬──────────────────┬───────┘
       │                  │
┌──────▼───────┐  ┌───────▼────────────┐
│ Repository   │  │ Integration Layer  │
│ (DB access)  │  │ (External APIs)    │
└──────────────┘  └────────────────────┘
       │
┌──────▼─────────────────┐
│  Database (PostgreSQL)  │
└─────────────────────────┘
```

**8-step pipeline this backend supports:**

| Step | Action | Key Components |
|---|---|---|
| 1 | Prompt Input | [prompt_routes.py](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py) → [PromptService](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#22-100) |
| 2 | Parse Prompt | `PromptService.parse_prompt()` + [parser.py](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py) |
| 3 | Fetch Confluence/Jira | [ConfluenceClient](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#17-65), [JiraClient](file:///d:/Testing%20automation%20frontend/backend/app/integrations/jira_client.py#17-63) |
| 4 | AI Generation (BDD + Selenium) | [AIService](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#25-104) → 4 agents → [generation_tasks.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py) |
| 5 | Review & Approval | [testcase_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/testcase_routes.py) → [TestCaseService](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#20-130) |
| 6 | Push to Zephyr | [zephyr_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/zephyr_routes.py) → [ZephyrService](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py#18-68) → [ZephyrClient](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#18-79) |
| 7 | Execute via Harness | [execution_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/execution_routes.py) → [ExecutionService](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#20-86) → [HarnessClient](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#18-84) |
| 8 | Fetch Results + AI Insights | [execution_tasks.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py) → `AIService.generate_ai_insights()` |

---

## Root-Level Files

### [requirements.txt](file:///d:/Testing%20automation%20frontend/backend/requirements.txt)
Lists every Python package the project depends on, grouped by purpose:

| Group | Key Packages |
|---|---|
| Web framework | `fastapi`, `uvicorn[standard]` |
| Database | `sqlalchemy`, `alembic`, `asyncpg`, `psycopg2-binary` |
| Cache / Queue | `redis`, [celery](file:///d:/Testing%20automation%20frontend/backend/app/tasks/celery_app.py#26-64), `flower` |
| AI / LLM | `langchain`, `langchain-google-genai`, `chromadb`, `tiktoken` |
| Validation | `pydantic`, `pydantic-settings` |
| Security | `python-jose`, `passlib` |
| HTTP clients | `httpx`, `aiohttp` |
| Utilities | `python-dotenv`, `structlog`, `orjson` |
| Testing | `pytest`, `pytest-asyncio`, `factory-boy` |

---

### [.env.example](file:///d:/Testing%20automation%20frontend/backend/.env.example)
Template for all environment variables. Copy to `.env` and fill in real values. **Never commit `.env` to version control.**

Groups covered:
- **Application** — `APP_NAME`, `APP_ENV`, `DEBUG`, `SECRET_KEY`
- **Database** — `DATABASE_URL`, pool sizing
- **Redis** — `REDIS_URL`, separate broker/result backend URLs
- **AI / LLM** — `GOOGLE_API_KEY`, model name, temperature, max tokens
- **Jira** — base URL, API token, user email, project key
- **Confluence** — base URL, API token, user email
- **Zephyr Scale** — base URL, API token, project key
- **Harness** — base URL, API key, account/org/project/pipeline IDs
- **JWT Auth** — algorithm, token expiry minutes/days
- **CORS** — allowed frontend origins
- **Logging** — level and output format (JSON or text)

---

### [Dockerfile](file:///d:/Testing%20automation%20frontend/backend/Dockerfile)
Multi-stage build that creates a minimal production Docker image.

**Stage 1 — Builder:**
- Starts from `python:3.11-slim`
- Installs `build-essential` and `libpq-dev` (needed to compile some Python packages)
- Creates an isolated virtual environment at `/opt/venv`
- Runs `pip install -r requirements.txt` inside the venv

**Stage 2 — Runtime:**
- Starts from a fresh `python:3.11-slim` (no build tools = smaller image)
- Copies only the venv from Stage 1 (avoids shipping compilers)
- Copies the application source ([app/](file:///d:/Testing%20automation%20frontend/src/pages/ReviewPage.vue#183-189), `alembic/`, [alembic.ini](file:///d:/Testing%20automation%20frontend/backend/alembic.ini))
- Creates a non-root `appuser` for security
- Exposes port `8000` and defaults to `uvicorn app.main:app`

---

### [docker-compose.yml](file:///d:/Testing%20automation%20frontend/backend/docker-compose.yml)
Defines the full local development stack with 6 services:

| Service | Purpose | Port |
|---|---|---|
| `api` | FastAPI application (hot-reload in dev) | 8000 |
| `worker` | Celery task worker (4 concurrent processes) | — |
| `beat` | Celery Beat scheduler (periodic tasks) | — |
| `flower` | Celery task monitoring UI | 5555 |
| `db` | PostgreSQL 16 with health check | 5432 |
| `redis` | Redis 7 for broker + cache | 6379 |

All services load from `.env` via `env_file`. The `api` service depends on `db` and `redis` with health checks so it only starts when they're truly ready.

---

### [alembic.ini](file:///d:/Testing%20automation%20frontend/backend/alembic.ini)
Configuration file read by Alembic during migration commands.

Key settings:
- `script_location = alembic` — points to the migration scripts folder
- `file_template` — names new migration files by date + hash + slug
- Logging configuration for Alembic's own output

The `sqlalchemy.url` here is a placeholder; the real URL is injected programmatically from the `DATABASE_URL` environment variable inside [alembic/env.py](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py).

---

### [README.md](file:///d:/Testing%20automation%20frontend/backend/README.md)
Project overview document for new developers. Contains:
- Tech stack table
- Folder structure diagram
- Quick-start instructions (copy `.env`, `docker compose up`, run migrations)
- Table of all planned API endpoints
- Description of each architecture layer

---

## `scripts/` — Shell Helper Scripts

### [scripts/start.sh](file:///d:/Testing%20automation%20frontend/backend/scripts/start.sh)
Starts the FastAPI Uvicorn server. Accepts optional CLI flags (e.g. `--reload`, `--workers N`). Key environment variables it respects: `HOST`, `PORT`, `LOG_LEVEL`, `WORKERS`. Run directly on bare metal: `./scripts/start.sh --reload`.

### [scripts/worker.sh](file:///d:/Testing%20automation%20frontend/backend/scripts/worker.sh)
Starts a Celery worker process. Configurable via `CONCURRENCY` (default 4), `QUEUES` (default: `generation,zephyr,execution,default`), and `LOG_LEVEL`. Called inside the Docker `worker` container.

### [scripts/migrate.sh](file:///d:/Testing%20automation%20frontend/backend/scripts/migrate.sh)
Wrapper for Alembic migration commands. Default action is `upgrade head` (apply all pending migrations). Accepts any Alembic sub-command: `revision`, `downgrade`, etc. Called inside the Docker `api` container before the server starts.

---

## `alembic/` — Database Migrations

### [alembic/env.py](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py)
The Alembic migration environment. This is the bridge between your SQLAlchemy models and the migration engine.

**Key responsibilities:**

1. **Model Import** — All ORM models ([User](file:///d:/Testing%20automation%20frontend/src/types/index.ts#128-135), [TestCase](file:///d:/Testing%20automation%20frontend/src/types/index.ts#8-22), [Execution](file:///d:/Testing%20automation%20frontend/src/types/index.ts#42-51), [ZephyrSync](file:///d:/Testing%20automation%20frontend/backend/app/models/zephyr.py#18-51)) must be imported here so Alembic can detect schema changes during `autogenerate`.

2. **URL Injection** — Reads `DATABASE_URL` from the environment and converts it from the async format (`postgresql+asyncpg://...`) to the sync format (`postgresql://...`) that Alembic requires.

3. **Offline Mode** ([run_migrations_offline](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py#50-64)) — Generates raw SQL statements to a file without a live DB connection. Useful for DBA review before applying changes.

4. **Online Mode** ([run_migrations_online](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py#66-78)) — Connects to the live database and applies migrations directly. This is the standard `alembic upgrade head` path used in CI/CD.

---

## [app/](file:///d:/Testing%20automation%20frontend/src/pages/ReviewPage.vue#183-189) — Application Source

### [app/main.py](file:///d:/Testing%20automation%20frontend/backend/app/main.py)
The application entry point. Every request flows through this file.

**[create_app() → FastAPI](file:///d:/Testing%20automation%20frontend/backend/app/main.py#49-69)**
Factory function that instantiates the FastAPI app. Using a factory (instead of a module-level `app = FastAPI()`) makes it easy to create multiple app instances for testing with different configurations.

**[lifespan(app)](file:///d:/Testing%20automation%20frontend/backend/app/main.py#26-45) (async context manager)**
Handles startup and shutdown events:
- *Startup*: configure logging, warm up DB pool, initialise vector store, verify external service connectivity
- *Shutdown*: close DB connections, flush Celery task queue, release Redis connections

**[_register_middleware(app)](file:///d:/Testing%20automation%20frontend/backend/app/main.py#71-90)**
Attaches middleware to the app in the correct order:
- **CORS** — allows the Vue frontend (`localhost:5173`) to call the API
- **RequestIDMiddleware** (placeholder) — adds a unique `X-Request-ID` header to every request for distributed tracing
- **TimingMiddleware** (placeholder) — logs request duration for performance monitoring

**[_register_routers(app)](file:///d:/Testing%20automation%20frontend/backend/app/main.py#92-101)**
Includes `api_router` at the `/api/v1` prefix, which in turn wires all 5 route groups (prompt, testcases, zephyr, execution, health).

---

## `app/core/` — Core Infrastructure

### [app/core/config.py](file:///d:/Testing%20automation%20frontend/backend/app/core/config.py)
Centralised configuration using **Pydantic Settings**. This is the single source of truth for every configuration value in the application.

**`class Settings(BaseSettings)`**
Reads all configuration from environment variables (or the `.env` file). Each field has a type annotation and a default value. Groups of settings:

| Group | Fields |
|---|---|
| Application | `APP_NAME`, `APP_ENV`, `DEBUG`, `SECRET_KEY`, `API_V1_PREFIX` |
| Database | `DATABASE_URL`, `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW` |
| Redis / Celery | `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` |
| AI | `GOOGLE_API_KEY`, `LLM_MODEL`, `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `EMBEDDING_MODEL` |
| Jira | `JIRA_BASE_URL`, `JIRA_API_TOKEN`, `JIRA_USER_EMAIL`, `JIRA_PROJECT_KEY` |
| Confluence | `CONFLUENCE_BASE_URL`, `CONFLUENCE_API_TOKEN`, `CONFLUENCE_USER_EMAIL` |
| Zephyr | `ZEPHYR_BASE_URL`, `ZEPHYR_API_TOKEN`, `ZEPHYR_PROJECT_KEY` |
| Harness | `HARNESS_BASE_URL`, `HARNESS_API_KEY`, all IDs |
| JWT | `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` |
| CORS | `ALLOWED_ORIGINS` (list of frontend URLs) |
| Logging | `LOG_LEVEL`, `LOG_FORMAT` |

**[get_settings() → Settings](file:///d:/Testing%20automation%20frontend/backend/app/core/config.py#101-111)** (cached with `@lru_cache`)
Returns a singleton [Settings](file:///d:/Testing%20automation%20frontend/backend/app/core/config.py#16-99) instance. The `.env` file is read only once per process.

**[settings](file:///d:/Testing%20automation%20frontend/backend/app/core/config.py#101-111)** (module-level)
A pre-instantiated singleton imported throughout the app:
```python
from app.core.config import settings
print(settings.DATABASE_URL)
```

---

### [app/core/security.py](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py)
All authentication and authorisation logic lives here.

**`class PasswordHasher`**
Wraps the `passlib` bcrypt library:
- [hash(plain_password)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#31-34) — returns a bcrypt-hashed string to store in the DB
- [verify(plain, hashed)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#35-38) — compares a login attempt against the stored hash (constant-time comparison)

**[create_access_token(subject, expires_delta)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#42-54)**
Creates a signed JWT access token. The token payload contains:
- `sub` (subject): user ID or email
- `exp`: expiry timestamp (`now + ACCESS_TOKEN_EXPIRE_MINUTES`)
- Signed with `SECRET_KEY` using `JWT_ALGORITHM` (HS256)

**[create_refresh_token(subject)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#56-67)**
Same as access token but with `REFRESH_TOKEN_EXPIRE_DAYS` expiry. Used to issue a new access token without re-login.

**[decode_token(token)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#69-83)**
Decodes and validates a JWT. Raises `HTTPException 401` if: token is expired, signature is invalid, or required claims are missing.

**[get_current_user(token)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#87-106) (FastAPI Dependency)**
Extracts the current user from the Bearer token in the `Authorization` header. Used as `Depends(get_current_user)` in protected route handlers. Returns the User ORM instance or raises 401.

**[get_current_admin_user(current_user)](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#108-116) (FastAPI Dependency)**
Chains on [get_current_user](file:///d:/Testing%20automation%20frontend/backend/app/core/security.py#87-106) and additionally checks `user.role == UserRole.ADMIN`. Raises 403 if not an admin.

---

### [app/core/logging.py](file:///d:/Testing%20automation%20frontend/backend/app/core/logging.py)
Structured logging configuration using the `structlog` library.

**[configure_logging(log_level, log_format)](file:///d:/Testing%20automation%20frontend/backend/app/core/logging.py#25-36)**
Called once at application startup inside [lifespan()](file:///d:/Testing%20automation%20frontend/backend/app/main.py#26-45). Sets up the `structlog` processing pipeline:
- *Development*: colourised, human-readable key=value output
- *Production* (`log_format="json"`): newline-delimited JSON — each log line is a parseable JSON object ready for ingestion by Datadog, CloudWatch, or Grafana Loki

**[get_logger(name)](file:///d:/Testing%20automation%20frontend/backend/app/core/logging.py#38-53)**
Returns a `BoundLogger` instance for a specific module. Use `__name__` as the name convention so log lines include the originating module. Example usage:
```python
logger = get_logger(__name__)
logger.info("testcase.approved", testcase_id="TC-001", user_id="u1")
```

**`class RequestIDFilter(logging.Filter)`**
A standard-library `logging.Filter` that injects the current HTTP request ID (from a `contextvars.ContextVar`) into every log record. This correlates all log lines within a single request, enabling distributed tracing.

---

### [app/core/constants.py](file:///d:/Testing%20automation%20frontend/backend/app/core/constants.py)
All magic strings and numbers are defined here as named constants. Import from here instead of hardcoding strings anywhere.

**`class TestCaseStatus(str, Enum)`**
Lifecycle states for a test case:
- `DRAFT` → initial AI-generated state
- `PENDING` → submitted for review
- `APPROVED` → approved, ready for Zephyr sync
- `REJECTED` → rejected with a reason

**`class TestCaseType(str, Enum)`**
Category of a test case. Controls which agents/frameworks are used:
- `UI` → Selenium WebDriver
- `API` → REST-Assured / httpx
- `REGRESSION` → full regression suite

**`class ExecutionStatus(str, Enum)`**
Status of a Harness pipeline execution: `PENDING → RUNNING → PASSED | FAILED | CANCELLED`

**`class SyncStatus(str, Enum)`**
Zephyr synchronisation state: `NOT_SYNCED → SYNCING → SYNCED | FAILED`

**`class UserRole(str, Enum)`**
RBAC roles: `ADMIN`, `TESTER`, `VIEWER`

**`class GenerationStage(str, Enum)`**
Stages of the AI generation pipeline, used to report progress to the `/prompt/status/{task_id}` polling endpoint.

**Numeric constants:**
- `MAX_PROMPT_LENGTH = 10_000` characters
- `MAX_FILE_SIZE_BYTES = 10 MB`
- `MAX_TESTCASES_PER_GENERATION = 50`
- `DEFAULT_PAGE_SIZE = 20`, `MAX_PAGE_SIZE = 100`
- `API_TIMEOUT_SECONDS = 30`, `GENERATION_TIMEOUT_SECONDS = 300`

**Queue name strings:**
- `QUEUE_GENERATION`, `QUEUE_ZEPHYR`, `QUEUE_EXECUTION`, `QUEUE_DEFAULT`
Used in Celery task routing configuration.

---

## `app/models/` — Database ORM Models

> All models extend SQLAlchemy's [Base](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#14-20) (not yet wired — [Base](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#14-20) import is commented out).
> Column definitions are shown as comments to keep the scaffold at zero import errors.

### [app/models/user.py](file:///d:/Testing%20automation%20frontend/backend/app/models/user.py)

**`class User`** — maps to the `users` table.

| Column | Type | Purpose |
|---|---|---|
| [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217) | UUID (PK) | Auto-generated primary key |
| [email](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#44-52) | String, unique, indexed | Login identifier |
| `hashed_pw` | String | bcrypt hash — never returned in API |
| `full_name` | String, nullable | Display name |
| `role` | UserRole enum | Access level |
| `is_active` | Boolean | Soft-delete flag (inactive = cannot log in) |
| `created_at` | DateTime(tz) | Creation timestamp |
| `updated_at` | DateTime(tz) | Auto-updated on every save |

**Relationships:**
- [test_cases](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#30-52) → list of [TestCase](file:///d:/Testing%20automation%20frontend/src/types/index.ts#8-22) objects created by this user
- [executions](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#81-86) → list of [Execution](file:///d:/Testing%20automation%20frontend/src/types/index.ts#42-51) objects triggered by this user

---

### [app/models/testcase.py](file:///d:/Testing%20automation%20frontend/backend/app/models/testcase.py)

**`class TestCase`** — maps to the [test_cases](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#30-52) table. Central entity of the platform.

| Column | Type | Purpose |
|---|---|---|
| [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217) | UUID (PK) | Primary key |
| [title](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106) | String(512) | Short descriptive title |
| `description` | Text | Full requirement description |
| `type` | TestCaseType enum | UI / API / Regression |
| [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60) | TestCaseStatus enum | Lifecycle status |
| `bdd_content` | Text | Gherkin feature file (BDDAgent output) |
| [selenium_code](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#72-84) | Text | Java Selenium/TestNG code (SeleniumAgent output) |
| `tags` | ARRAY(String) | Searchable labels (smoke, auth, checkout…) |
| [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39) | String(128) | Zephyr Scale test case ID (set after sync) |
| `sync_status` | SyncStatus enum | Zephyr sync state |
| `created_by_id` | UUID (FK → users) | Owner/creator |
| `created_at` / `updated_at` | DateTime | Timestamps |

---

### [app/models/execution.py](file:///d:/Testing%20automation%20frontend/backend/app/models/execution.py)

**`class Execution`** — maps to the [executions](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#81-86) table. Represents a single Harness pipeline run.

| Column | Type | Purpose |
|---|---|---|
| [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217) | UUID (PK) | Primary key |
| `harness_run_id` | String, indexed | ID returned by Harness (used for status polling) |
| `pipeline_id` | String | Harness pipeline identifier |
| [environment](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#84-94) | String | staging / qa / production |
| [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60) | ExecutionStatus enum | Current run state |
| [test_case_ids](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30) | ARRAY(String) | Which test cases are in this run |
| `total_tests` | Integer | Count of test cases |
| `passed_count` | Integer | Passed tests |
| `failed_count` | Integer | Failed tests |
| `pass_rate` | Float | 0.0–100.0 percentage |
| `duration_seconds` | Float | Wall-clock time |
| [logs](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#55-65) | JSON | Array of `{timestamp, level, message}` dicts |
| [results](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#61-71) | JSON | Array of per-test result dicts |
| `triggered_by_id` | UUID (FK → users) | User who triggered |
| `started_at` / `completed_at` | DateTime | Run timestamps |

---

### [app/models/zephyr.py](file:///d:/Testing%20automation%20frontend/backend/app/models/zephyr.py)

**`class ZephyrSync`** — maps to the `zephyr_syncs` table. One record per test case sync attempt.

| Column | Type | Purpose |
|---|---|---|
| [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217) | UUID (PK) | Primary key |
| [test_case_id](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30) | UUID (FK → test_cases) | Which test case was synced |
| [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39) | String | Zephyr's test case ID after creation |
| `project_key` | String | Zephyr project (e.g. "ESHOP") |
| `sync_status` | SyncStatus enum | Current sync state |
| `error_message` | Text | Error detail if sync failed |
| `synced_at` | DateTime | Last successful sync timestamp |
| `created_at` | DateTime | Record creation |

Provides a full audit trail of every sync attempt, including re-sync operations.

---

## `app/schemas/` — Pydantic Request/Response Schemas

> Schemas validate input and shape output. They are *intentionally* separate from ORM models so the API contract can evolve independently of the DB schema.

### [app/schemas/prompt_schema.py](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py)

**[PromptGenerateRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py#18-48)** — body for `POST /api/v1/prompt/generate`:
- [prompt_text](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#51-66): required free-text description
- [confluence_url](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#39-47): optional `HttpUrl` validated URL
- [jira_ticket](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#27-38): optional Jira key (validated against `PROJECT-NNNN` pattern)
- `test_type`: "UI" | "API" | "Regression"
- [generate_bdd](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#59-71) / [generate_selenium](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#72-84): boolean toggles

Includes two `@field_validator` methods:
- [validate_prompt_length](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py#37-42) — enforces `MAX_PROMPT_LENGTH`
- [validate_jira_format](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py#43-48) — rejects malformed ticket keys

**[ParsedInputResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py#50-62)** — response for `/prompt/parse`:
- `confluence_links`, [jira_tickets](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#27-38), `prompt_summary`

**[GenerationStatusResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/prompt_schema.py#64-78)** — response for `/prompt/status/{task_id}`:
- [task_id](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#41-44), `stage` (GenerationStage), [progress](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#65-68) (0–100), `message`

---

### [app/schemas/testcase_schema.py](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py)

**[TestCaseBase](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#14-20)** — shared fields (inherited by create/response): [title](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106), `description`, `type`, `tags`

**[TestCaseCreateRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#24-31)** — manual test case creation body; adds `bdd_content`, [selenium_code](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#72-84)

**[TestCaseUpdateRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#33-50)** — partial update body for `PATCH /{id}`; all fields optional

**[TestCaseStatusUpdateRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#52-63)** — for `PATCH /{id}/status`: [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60) and optional `reason`

**[TestCaseResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#67-82)** — full detail response; includes all columns plus `sync_status`, [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39), timestamps. Has `model_config = {"from_attributes": True}` to enable direct construction from ORM instances.

**[TestCaseListResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/testcase_schema.py#84-91)** — pagination envelope: `items`, [total](file:///d:/Testing%20automation%20frontend/backend/tests/services/test_testcase_service.py#34-37), [page](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#44-52), `page_size`, `has_next`

---

### [app/schemas/execution_schema.py](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py)

**[ExecutionRunRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#15-27)** — trigger body: [test_case_ids](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30) list, optional `pipeline_id`, [environment](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#84-94)

**[LogEntry](file:///d:/Testing%20automation%20frontend/src/types/index.ts#52-57)** — single log line: `timestamp`, `level` (info/success/error/warn/action), `message`

**[AIInsightSchema](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#38-52)** — AI root cause analysis result:
- `root_cause`: plain-language explanation of failure
- `suggested_fix`: recommended code/config change
- `impacted_tests`: other test IDs likely affected
- `confidence`: 0.0–1.0 AI confidence score

**[TestResultSchema](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#54-64)** — full result for one test case:
- [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), `duration_ms`, [logs](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#55-65) (list of LogEntry), `screenshots`, `artifacts`, optional [ai_insight](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#85-97)

**[ExecutionResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#68-74)** — initial trigger acknowledgement: `execution_id`, [task_id](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#41-44), [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), `message`

**[ExecutionStatusResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#76-83)** — live status poll response: [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), [progress](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#65-68), [logs](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#55-65)

**[ExecutionResultsResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#85-100)** — final results: summary statistics + [results](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#61-71) list of [TestResultSchema](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#54-64)

---

### [app/schemas/zephyr_schema.py](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py)

**[ZephyrPushRequest](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#14-26)** — [test_case_ids](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30), optional `project_key`, optional `folder_name`

**[ZephyrConnectionStatus](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#30-40)** — `/status` response: `connected`, `project_key`, [base_url](file:///d:/Testing%20automation%20frontend/backend/alembic/env.py#39-48), `last_sync`, [error](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#42-55)

**[ZephyrSyncResult](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#42-49)** — single sync outcome: [test_case_id](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30), [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39), `sync_status`, [error](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#42-55)

**[ZephyrPushResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#51-60)** — bulk push summary: `total_requested`, `pushed_count`, `failed_count`, [results](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#61-71)

**[ZephyrTestCaseResponse](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#62-75)** — synced test case for display: [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39), `sync_status`, `synced_at`

---

## `app/api/v1/` — HTTP API Layer

### [app/api/v1/api_router.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/api_router.py)
The single aggregator for all route groups. This file is included in [main.py](file:///d:/Testing%20automation%20frontend/backend/app/main.py) at the `/api/v1` prefix. Adding a new feature means: (1) create its route file, (2) import its router here, (3) call `api_router.include_router()`. No other files need to change.

---

### [app/api/v1/routes/health_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/health_routes.py)
Operator-facing health check endpoints.

**`GET /health/`** — Liveness probe. Returns HTTP 200 if the process is alive. Used by Kubernetes to decide if a pod needs restarting.

**`GET /health/ready`** — Readiness probe. Returns HTTP 200 only when the app can serve traffic (DB connection pool available). Used by Kubernetes to route traffic.

**`GET /health/detailed`** — Deep health check. Tests DB (SELECT 1), Redis (PING), and Celery worker availability. Returns a status dict per dependency (`healthy | degraded | unhealthy`). Useful for dashboards and alerting.

---

### [app/api/v1/routes/prompt_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/prompt_routes.py)
Handles **Steps 1–2** of the pipeline (Prompt Input → Parse → Trigger Generation).

**`POST /prompt/parse`** — Synchronous fast path. Parses the submitted prompt and returns a preview of detected Confluence links, Jira tickets, and a short AI summary. Used by the frontend to show users what was detected before they click Generate.

**`POST /prompt/generate`** — Async trigger path. Validates input, then dispatches the Celery task chain (parse → fetch → generate BDD → generate Selenium). Returns immediately with a [task_id](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#41-44) for polling. HTTP 202 Accepted.

**`GET /prompt/status/{task_id}`** — Polling endpoint. Checks the Celery task's Redis state and returns the current `stage`, [progress](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#65-68) (0–100), and a `message`. The Processing page in the UI calls this every 2 seconds.

---

### [app/api/v1/routes/testcase_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/testcase_routes.py)
CRUD + lifecycle management for test cases (**Steps 5–6**: Review and Approval).

| Endpoint | Purpose |
|---|---|
| `GET /testcases/` | Paginated list with [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60), `type`, and [search](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#54-66) filters |
| `POST /testcases/` | Manual creation (for importing existing tests) |
| `GET /testcases/{id}` | Full detail including BDD + Selenium content |
| `PATCH /testcases/{id}` | Partial update of any field (inline editing in Review page) |
| `DELETE /testcases/{id}` | Hard delete; blocked if test is in an active execution |
| `PATCH /testcases/{id}/status` | Approve or reject with optional rejection reason |
| `POST /testcases/{id}/regenerate` | Re-trigger AI generation for a single test case |

---

### [app/api/v1/routes/zephyr_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/zephyr_routes.py)
Zephyr Scale integration endpoints (**Step 6**: Push to Zephyr).

| Endpoint | Purpose |
|---|---|
| `GET /zephyr/status` | Check connection, verify credentials, return last sync time |
| `GET /zephyr/synced` | List all test cases with `sync_status=synced` and their Zephyr IDs |
| `POST /zephyr/push` | Bulk push selected approved test cases |
| `POST /zephyr/push/{id}` | Push a single test case ("Re-sync" button) |

---

### [app/api/v1/routes/execution_routes.py](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/execution_routes.py)
Harness pipeline execution endpoints (**Steps 7–8**: Execute + Results).

| Endpoint | Method | Purpose |
|---|---|---|
| `/execution/run` | POST | Trigger async Harness execution; returns `execution_id` + [task_id](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#41-44) |
| `/execution/{id}/status` | GET | Live status + accumulated logs for a running execution |
| `/execution/{id}/results` | GET | Full results including per-test outcomes and AI insights |
| `/execution/{id}/cancel` | POST | Cancel a running Harness pipeline |
| `/execution/` | GET | Paginated history of all past executions |

---

## `app/services/` — Business Logic Layer

Services contain the "what" of the application. They call repositories for DB access and integration clients for external APIs. Route handlers never call repositories or clients directly.

### [app/services/prompt_service.py](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py)

**`class PromptService`** — orchestrates **Steps 1–4**.

**[parse_prompt(input_text)](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/prompt_routes.py#22-39)**
Runs the raw user input through [PromptParser](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#17-56) to extract:
- Confluence page URLs (regex)
- Jira ticket keys (`[A-Z]+-\d+` regex)
- Cleans/normalises the text

**[enrich_context(parsed)](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#58-72)**
Calls `ConfluenceClient.get_page_by_url()` and `JiraClient.get_issue()` in parallel for all detected links/tickets. Returns an enriched context dict that includes the full page/ticket text as additional context for the LLM.

**[trigger_generation(enriched_context, options)](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#73-88)**
Dispatches the Celery task chain:
```
parse_and_enrich_task → generate_testcases_task → generate_bdd_task → generate_selenium_task
```
Returns the Celery [task_id](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#41-44) immediately so the frontend can start polling.

**[get_generation_status(task_id)](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#89-100)**
Queries Celery's Redis backend for the task's current state. Maps internal Celery states to [GenerationStage](file:///d:/Testing%20automation%20frontend/backend/app/core/constants.py#75-88) values and returns a progress percentage.

---

### [app/services/testcase_service.py](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py)

**`class TestCaseService`** — lifecycle management for **Steps 5–6**.

**[list_test_cases(...)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#30-52)**
Delegates to `TestCaseRepository.list()` with pagination and filters. Returns the paginated response envelope.

**[get_test_case(id)](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/testcase_routes.py#56-65)**
Calls `repo.get_by_id()`. Raises `HTTPException 404` if not found.

**[create_test_case(data, created_by_id)](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/testcase_routes.py#47-54)**
Runs duplicate detection via [detect_duplicates()](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#110-118) before persisting. Returns the created instance.

**[update_test_case(id, patch)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#75-87)**
Validates that the test case exists, then calls `repo.update()` with only the non-None patch fields.

**[delete_test_case(id)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#88-96)**
Checks that the test case is not referenced by any `RUNNING` execution before deleting. Raises `HTTPException 409` if it is.

**[update_status(id, new_status, reason)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#97-109)**
Enforces the allowed transition graph:
```
draft    → pending
pending  → approved | rejected
rejected → pending
```
Raises `HTTPException 409` for disallowed transitions. Stores rejection reason for auditability.

**[detect_duplicates(title)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#110-118)**
Calls `repo.find_by_title_similarity()` to check if a very similar test case already exists. Returns a list of potential duplicate IDs.

**[bulk_approve(test_case_ids)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#119-130)**
Calls `repo.bulk_update_status()` for efficiency (single SQL UPDATE). Returns the count of updated rows.

---

### [app/services/zephyr_service.py](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py)

**`class ZephyrService`** — orchestrates **Step 6**.

**[check_connection()](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#28-36)**
Calls `ZephyrClient.check_connection()`. Maps the result to a [ZephyrConnectionStatus](file:///d:/Testing%20automation%20frontend/backend/app/schemas/zephyr_schema.py#30-40) dict including the last sync timestamp from the DB.

**[push_test_cases(test_case_ids, project_key)](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py#37-53)**
For each test case:
1. Fetch full detail from DB
2. If [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39) exists → call `ZephyrClient.update_test_case()`
3. Otherwise → call `ZephyrClient.create_test_case()`, save returned ID
4. Update `sync_status` and [zephyr_id](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py#36-39) in DB

Handles partial failures: continues through the list even if individual pushes fail. Returns a summary with `pushed_count` and `failed_count`.

**[push_single(id)](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py#54-62)**
Same logic as [push_test_cases()](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py#37-53) but for a single test case (Re-sync button).

**[get_synced_test_cases()](file:///d:/Testing%20automation%20frontend/backend/app/services/zephyr_service.py#63-68)**
Queries [TestCaseRepository](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#18-115) for all test cases where `sync_status = SYNCED`.

---

### [app/services/execution_service.py](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py)

**`class ExecutionService`** — orchestrates **Steps 7–8**.

**[trigger_execution(test_case_ids, pipeline_id, environment)](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#30-49)**
Creates an [Execution](file:///d:/Testing%20automation%20frontend/src/types/index.ts#42-51) DB record with status `PENDING`, then dispatches `execution_tasks.run_harness_pipeline_task.delay(...)`. Returns `{execution_id, task_id}`.

**[get_status(execution_id)](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60)**
If the execution is `RUNNING`, calls `HarnessClient.get_execution_logs()` to fetch fresh log lines and appends them to the DB. Returns the accumulated logs with current status.

**[get_results(execution_id)](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#61-71)**
Returns the complete results. If AI insights haven't been generated yet (they run asynchronously), re-triggers [generate_ai_insights_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py#48-62). Raises 409 if execution isn't complete.

**[cancel_execution(execution_id)](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#72-80)**
Calls `HarnessClient.cancel_pipeline(harness_run_id)`, revokes the Celery task, and updates the DB status to `CANCELLED`.

**[list_executions(page, page_size)](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#81-86)**
Returns paginated history via `ExecutionRepository.list()`, most recent first.

---

### [app/services/ai_service.py](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py)

**`class AIService`** — unified facade over all AI/LLM capabilities. This is the most critical service.

**[__init__()](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#23-26)**
Initialises the Google Gemini LLM client (via LangChain), the embedding model, and singleton instances of all four agents. Called once per Celery worker process.

**[generate_test_cases(context, options)](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#40-58)**
Runs the full 4-agent pipeline sequentially:
1. `RequirementAgent.extract_requirements()` → structured requirement list
2. `TestCaseAgent.generate()` → structured test case dicts
3. `BDDAgent.generate_batch()` → Gherkin for each test case (concurrent)
4. `SeleniumAgent.generate_batch()` → Java code for each test case (concurrent)

Returns fully populated test case dicts ready for DB insertion.

**[generate_bdd(title, context)](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#59-71)**
Single-test-case wrapper around `BDDAgent.generate()`. Used when regenerating one test case.

**[generate_selenium_code(bdd_content, test_type)](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#72-84)**
Single-test-case wrapper around `SeleniumAgent.generate()`.

**[generate_ai_insights(failed_test, logs)](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#85-97)**
Constructs a targeted prompt that includes the failed test's BDD scenario, Selenium code, and execution logs. Calls the LLM and parses the response into an [AIInsightSchema](file:///d:/Testing%20automation%20frontend/backend/app/schemas/execution_schema.py#38-52) dict: `{root_cause, suggested_fix, impacted_tests, confidence}`.

**[get_similar_test_cases(query, top_k)](file:///d:/Testing%20automation%20frontend/backend/app/services/ai_service.py#98-104)**
Delegates to `RAGRetriever.get_relevant_context()` for duplicate detection and context enrichment.

---

## `app/repositories/` — Database Access Layer

Repositories contain all SQLAlchemy queries. Services never write raw SQL or ORM queries — only repositories do.

### [app/repositories/testcase_repo.py](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py)

**`class TestCaseRepository`**

| Method | SQL Operation |
|---|---|
| [create(data)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#23-34) | `INSERT INTO test_cases ...` |
| [get_by_id(id)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#35-43) | `SELECT ... WHERE id = :id` |
| [list(page, size, status, type, search)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#76-84) | `SELECT ... WHERE ... LIMIT ... OFFSET ...` with `COUNT(*)` |
| [update(id, patch)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#53-62) | `UPDATE test_cases SET ... WHERE id = :id` |
| [delete(id)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#67-70) | `DELETE FROM test_cases WHERE id = :id` |
| [find_by_title_similarity(title, threshold)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106) | `SELECT ... WHERE similarity(title, :q) > :threshold ORDER BY similarity DESC` (PostgreSQL `pg_trgm` extension) |
| [bulk_update_status(ids, status)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#107-115) | `UPDATE test_cases SET status = :s WHERE id = ANY(:ids)` |

---

### [app/repositories/execution_repo.py](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py)

**`class ExecutionRepository`**

| Method | Purpose |
|---|---|
| [create(data)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#23-34) | Insert new Execution record |
| [get_by_id(id)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#35-43) | Fetch single execution |
| [update_status(id, status, extra)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#97-109) | Update status + optional fields (completed_at, pass_rate) |
| [append_logs(id, log_entries)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#55-65) | `jsonb_array_append` SQL to add logs without full rewrite |
| [save_results(id, results, summary)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#66-75) | Persist final per-test results + statistics |
| [list(page, size)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#76-84) | Paginated history, ORDER BY started_at DESC |

---

### [app/repositories/user_repo.py](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py)

**`class UserRepository`**

| Method | Purpose |
|---|---|
| [create(data)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#23-34) | Insert new user |
| [get_by_id(id)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#35-43) | PK lookup |
| [get_by_email(email)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#44-52) | Used during login to load user by email |
| [update(id, patch)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#53-62) | Profile update |
| [set_active(id, bool)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/user_repo.py#63-71) | Activate or soft-delete |
| [list(page, size)](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#76-84) | Admin: paginated user list |

---

## `app/integrations/` — External Service Clients

Each client is a thin HTTP wrapper. It knows nothing about business logic — it only makes HTTP calls, handles auth, and raises a typed `IntegrationError` on failure.

### [app/integrations/jira_client.py](file:///d:/Testing%20automation%20frontend/backend/app/integrations/jira_client.py)

**`class JiraClient`** — wraps the Atlassian Jira REST API v3.

**[get_issue(ticket_key)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/jira_client.py#27-41)**
`GET /rest/api/3/issue/{ticket_key}` with Basic authentication (base64 of `email:api_token`). Extracts and returns: `summary`, `description`, `acceptance_criteria` (from custom field), `labels`, `priority`.

**[search_issues(jql, max_results)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/jira_client.py#42-54)**
`POST /rest/api/3/issue/search` with a JQL query. Returns simplified issue list.

**[get_project_info(project_key)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/jira_client.py#55-63)**
`GET /rest/api/3/project/{key}`. Returns project metadata.

---

### [app/integrations/confluence_client.py](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py)

**`class ConfluenceClient`** — wraps the Atlassian Confluence REST API v2.

**[get_page_by_url(page_url)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#27-43)**
Parses the URL to extract the space key and page title. Calls `GET /wiki/rest/api/content?title=...&spaceKey=...`. Fetches the [storage](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#53-65) (XHTML) body format, then calls [_storage_to_plain_text()](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#53-65) to strip tags.

**[get_page_by_id(page_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#44-52)**
Direct lookup: `GET /wiki/rest/api/content/{id}?expand=body.storage`.

**[_storage_to_plain_text(storage_html)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/confluence_client.py#53-65)**
Internal method. Uses `BeautifulSoup` or `html.parser` to strip Confluence's XML/XHTML representation into clean plaintext. Handles special Confluence macros (code blocks, info panels, tables).

---

### [app/integrations/zephyr_client.py](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py)

**`class ZephyrClient`** — wraps the Zephyr Scale REST API v2 (SmartBear).

**[check_connection()](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#28-36)**
`GET /projects` — if the response is 200 and contains the configured project key, connectivity is confirmed.

**[create_test_case(project_key, title, bdd_content, test_type)](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/testcase_routes.py#47-54)**
`POST /testcases` — creates a new test case. Returns Zephyr's internal ID and the web URL.

**[update_test_case(zephyr_id, title, bdd_content)](file:///d:/Testing%20automation%20frontend/backend/app/services/testcase_service.py#75-87)**
`PUT /testcases/{id}` — updates an already-synced test case.

**[create_test_cycle(project_key, execution_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#64-72)**
`POST /testcycles` — creates a Zephyr test cycle linked to a Harness execution.

**[_with_retry(coro, max_retries)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#73-79)**
Internal async retry wrapper. Implements exponential backoff (1s, 2s, 4s) for `429 Rate Limit` and `5xx Server Error` responses.

---

### [app/integrations/harness_client.py](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py)

**`class HarnessClient`** — wraps the Harness Platform API.

**[trigger_pipeline(pipeline_id, inputs)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#28-40)**
`POST /pipelines/execute/{pipelineId}` with runtime input set. The `inputs` dict contains the test case IDs, environment, and any pipeline-specific variables. Returns `{run_id, execution_url}`.

**[get_execution_status(run_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#41-52)**
`GET /executions/{run_id}` — returns current status, stage breakdowns, and start/end times.

**[get_execution_logs(run_id, stage_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#53-65)**
`GET /executions/{run_id}/logs` — fetches log output for streaming to the UI.

**[cancel_pipeline(run_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#66-74)**
`POST /executions/{run_id}/abort` — sends a cancellation signal.

**[get_test_report(run_id)](file:///d:/Testing%20automation%20frontend/backend/app/integrations/harness_client.py#75-84)**
`GET /executions/{run_id}/testReport` — fetches the JUnit/TestNG test report artifact. Maps test names back to test_case_ids using naming conventions.

---

## `app/ai/` — AI & LLM Layer

### [app/ai/agents/requirement_agent.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/requirement_agent.py)

**`class RequirementAgent`** — Pipeline Step 1 within AI generation.

**[extract_requirements(enriched_context)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/requirement_agent.py#35-54)**
Constructs an LLM prompt that asks Gemini to read the combined Confluence + Jira + prompt text and output a clean JSON list of requirements. Each requirement has: [id](file:///d:/Testing%20automation%20frontend/src/pages/PromptInputPage.vue#202-217), [title](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#97-106), `description`, `priority`, `source`. Result feeds into [TestCaseAgent](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/testcase_agent.py#14-64).

**[_build_prompt(context)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/selenium_agent.py#65-71)**
Loads the base prompt from [app/ai/prompts/testcase_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/testcase_prompt.txt) (requirements extraction is handled in the same prompt template) and injects the enriched context.

---

### [app/ai/agents/testcase_agent.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/testcase_agent.py)

**`class TestCaseAgent`** — Pipeline Step 2 within AI generation.

**[generate(requirements, options)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#34-45)**
Sends the structured requirements list to the LLM with [testcase_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/testcase_prompt.txt). The LLM returns a JSON array of test case objects. This agent also validates the JSON schema of the response before returning.

**[_build_prompt(requirements, options)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/selenium_agent.py#65-71)**
Serialises the requirements list and injects `test_type` and `max_cases` options into the template.

---

### [app/ai/agents/bdd_agent.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py)

**`class BDDAgent`** — Pipeline Step 3 within AI generation.

**[generate(test_case)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#34-45)**
Calls the LLM with [bdd_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/bdd_prompt.txt), injecting the test case's title, description, steps, and expected outcome. Also injects RAG context (similar existing test cases) to guide the LLM toward established patterns in your codebase.

**[generate_batch(test_cases)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#46-57)**
Uses `asyncio.gather()` to generate BDD for all test cases concurrently, reducing latency significantly.

**[_validate_gherkin(content)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#65-71)**
Simple structural check: the output must contain at least one `Feature:` and one `Scenario:` keyword.

---

### [app/ai/agents/selenium_agent.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/selenium_agent.py)

**`class SeleniumAgent`** — Pipeline Step 4 within AI generation.

**[generate(bdd_content, test_case_title, test_type)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#34-45)**
Calls the LLM with [selenium_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/selenium_prompt.txt), injecting the Gherkin content and title. For `test_type=UI`, generates Selenium 4 + TestNG. For `test_type=API`, generates REST-Assured (Java HTTP client for API tests).

**[generate_batch(test_cases)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/bdd_agent.py#46-57)**
Concurrent generation via `asyncio.gather()`.

**[_sanitise_class_name(title)](file:///d:/Testing%20automation%20frontend/backend/app/ai/agents/selenium_agent.py#72-78)**
Converts a test case title like "User Login – Happy Path" to a valid Java class name `UserLoginHappyPath` (strips special characters, applies PascalCase).

---

### [app/ai/rag/vector_store.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py)

**`class VectorStore`** — ChromaDB wrapper for semantic search.

**[upsert(doc_id, text, metadata)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#34-44)**
Embeds the [text](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#64-79) using the configured Google Embedding model and stores the vector in ChromaDB with `doc_id` as the key. Called after each test case is generated or updated.

**[upsert_batch(documents)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#45-53)**
Bulk version for initial data loading or re-indexing. More efficient than individual upserts.

**[search(query, top_k)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#54-66)**
Embeds the query, performs approximate nearest-neighbour (ANN) search in ChromaDB, and returns the `top_k` most similar documents with their similarity scores.

**[delete(doc_id)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/vector_store.py#67-70)**
Called when a test case is deleted to keep the vector index clean.

---

### [app/ai/rag/retriever.py](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/retriever.py)

**`class RAGRetriever`** — high-level semantic search interface.

**[get_relevant_context(query, top_k, filters)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/retriever.py#35-48)**
Wraps `VectorStore.search()` with optional metadata filters (e.g. only search within UI test cases). Used in:
- `AIService.get_similar_test_cases()` — duplicate detection
- `BDDAgent._build_prompt()` — context injection for better BDD output
- `SeleniumAgent._build_prompt()` — context injection for consistent code style

**[format_for_prompt(documents)](file:///d:/Testing%20automation%20frontend/backend/app/ai/rag/retriever.py#49-67)**
Converts the list of retrieved documents into a formatted text block that can be directly embedded into LLM prompts as the "--- Similar Test Cases ---" section.

---

## `app/ai/prompts/` — LLM Prompt Templates

Plain [.txt](file:///d:/Testing%20automation%20frontend/backend/requirements.txt) files with `{placeholder}` variables injected at runtime.

### [testcase_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/testcase_prompt.txt)
Instructs the LLM to act as a QA engineer and generate 5–15 test cases from requirements. Specifies the exact JSON output format (array of `{title, description, type, tags, preconditions, steps, expected_outcome}`). Tells the LLM to return **only** the JSON array — no markdown fences.

### [bdd_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/bdd_prompt.txt)
Instructs the LLM to act as a BDD expert and convert a structured test case into a Gherkin feature file. Includes a `{rag_context}` placeholder for RAG-retrieved similar scenarios. Enforces strict Gherkin syntax requirements.

### [selenium_prompt.txt](file:///d:/Testing%20automation%20frontend/backend/app/ai/prompts/selenium_prompt.txt)
Instructs the LLM to act as a senior Java Selenium engineer. Specifies the Page Object Model pattern, TestNG annotations, WebDriverManager, explicit waits, and Javadoc requirements. Injects the BDD scenario as the spec for the code to implement.

---

## `app/tasks/` — Celery Async Workers

### [app/tasks/celery_app.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/celery_app.py)

**[create_celery() → Celery](file:///d:/Testing%20automation%20frontend/backend/app/tasks/celery_app.py#26-64)**
Factory function that creates the configured Celery instance.

Key configuration:
- **Broker**: Redis (task queue)
- **Result backend**: Redis (task result storage)
- **Serialiser**: JSON (human-readable and secure)
- **Task routing**: Each domain has its own queue ([generation](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#73-88), [zephyr](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/zephyr_routes.py#43-63), [execution](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/execution_routes.py#21-36), `default`). This allows you to scale each queue independently with separate worker processes.
- **`task_soft_time_limit`**: Raises `SoftTimeLimitExceeded` after 300s — tasks can catch this for graceful cleanup
- **`task_time_limit`**: Hard kill after 360s
- **`autodiscover_tasks`**: Automatically finds all `@celery.task` decorators in the task modules

**[celery](file:///d:/Testing%20automation%20frontend/backend/app/tasks/celery_app.py#26-64)** — the singleton instance imported by all task files.

---

### [app/tasks/generation_tasks.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py)

Four Celery tasks that form a **chain** (output of one is input of the next):

| Task | Queue | Soft Limit | Responsibility |
|---|---|---|---|
| [parse_and_enrich_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py#19-33) | generation | 120s | Parse prompt + fetch Confluence/Jira content |
| [generate_testcases_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py#36-50) | generation | 180s | Run RequirementAgent + TestCaseAgent |
| [generate_bdd_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py#53-64) | generation | 120s | Run BDDAgent for all test cases |
| [generate_selenium_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/generation_tasks.py#67-81) | generation | 180s | Run SeleniumAgent, persist to DB, index in vector store |

Each task updates a Redis key with `{stage, progress, message}` so the `/prompt/status/{task_id}` endpoint can return real-time progress.

---

### [app/tasks/zephyr_tasks.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/zephyr_tasks.py)

**[push_to_zephyr_task(test_case_ids, project_key)](file:///d:/Testing%20automation%20frontend/backend/app/tasks/zephyr_tasks.py#15-33)**
Runs on the [zephyr](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/zephyr_routes.py#43-63) queue. Processes each test case serially (to stay within Zephyr's rate limit). For each: calls [ZephyrClient](file:///d:/Testing%20automation%20frontend/backend/app/integrations/zephyr_client.py#18-79), persists the returned Zephyr ID, and updates `sync_status`. Uses `max_retries=5` with 30s default delay to handle transient API failures.

**[push_single_to_zephyr_task(test_case_id, project_key)](file:///d:/Testing%20automation%20frontend/backend/app/tasks/zephyr_tasks.py#36-45)**
Lightweight single-test-case version for Re-sync button actions.

---

### [app/tasks/execution_tasks.py](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py)

**[run_harness_pipeline_task(execution_id, test_case_ids, pipeline_id, environment)](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py#21-45)**
The most complex task. Runs on the [execution](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/execution_routes.py#21-36) queue. Full lifecycle:
1. Calls `HarnessClient.trigger_pipeline()` → stores returned `harness_run_id`
2. Polls `HarnessClient.get_execution_status()` every 10 seconds
3. On each poll, appends new log lines via `ExecutionRepository.append_logs()`
4. On completion: fetches test report, maps results to test case IDs, saves via [save_results()](file:///d:/Testing%20automation%20frontend/backend/app/repositories/execution_repo.py#66-75)
5. Dispatches [generate_ai_insights_task](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py#48-62) for each failed test case
6. Updates execution [status](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#50-60) to `PASSED` or `FAILED`

`SoftTimeLimitExceeded` handler: updates status to `FAILED` and cancels the Harness run.

**[generate_ai_insights_task(execution_id, failed_test)](file:///d:/Testing%20automation%20frontend/backend/app/tasks/execution_tasks.py#48-62)**
Runs on the [execution](file:///d:/Testing%20automation%20frontend/backend/app/api/v1/routes/execution_routes.py#21-36) queue. Calls `AIService.generate_ai_insights()` and writes the result back to the corresponding test result in the execution's JSON [results](file:///d:/Testing%20automation%20frontend/backend/app/services/execution_service.py#61-71) column.

---

## `app/utils/` — Shared Utilities

### [app/utils/parser.py](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py)

**`class PromptParser`**
Stateless utility used by `PromptService.parse_prompt()`.

- **`JIRA_TICKET_PATTERN`**: `r'\b([A-Z][A-Z0-9]+-\d+)\b'` — matches `ESHOP-4521`
- **`CONFLUENCE_URL_PATTERN`**: matches `atlassian.net/wiki` URLs
- [extract_jira_tickets(text)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#27-38) → unique list of matched ticket keys
- [extract_confluence_urls(text)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#39-47) → unique list of matched Confluence URLs
- [extract_all_urls(text)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#48-56) → all HTTP/HTTPS URLs

**`class FileParser`**
Used by the `/prompt/generate` endpoint when the user uploads a file.
- [extract_text(filename, content)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#64-79) — routes to the correct parser based on file extension
- [_extract_pdf(content)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#80-83) — uses `pdfminer` or `PyMuPDF`
- [_extract_docx(content)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#84-87) — uses `python-docx`
- [_extract_txt(content)](file:///d:/Testing%20automation%20frontend/backend/app/utils/parser.py#88-91) — UTF-8 decode

---

### [app/utils/formatter.py](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py)

**`class ResponseFormatter`**
Ensures all API responses share the same envelope shape. Services return raw data; route handlers wrap it using this formatter.

- [success(data, message)](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#28-41) → `{"success": true, "data": ..., "message": "..."}`
- [error(message, detail)](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#42-55) → `{"success": false, "error": "...", "detail": ...}`
- [paginated(items, total, page, size)](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#56-65) → `{"items": [...], "total": N, "page": N, "has_next": bool, "has_prev": bool}`

**[java_class_name(title)](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#67-81)**
Converts test case title to a valid Java PascalCase class name. Used by `SeleniumAgent._sanitise_class_name()`.

**[format_duration(seconds)](file:///d:/Testing%20automation%20frontend/backend/app/utils/formatter.py#83-93)**
Human-readable duration: `45.0 → "45s"`, `123.0 → "2m 3s"`, `3661.0 → "1h 1m 1s"`.

---

### [app/utils/validators.py](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py)

Standalone business-rule validation functions. Used in services before making DB or API calls.

| Function | Purpose |
|---|---|
| [validate_test_case_ids_exist(ids, existing)](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#13-30) | Returns list of missing IDs; service raises 404 if non-empty |
| [validate_status_transition(current, requested)](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#32-49) | Returns `True` if transition is in the allowed graph; service raises 409 if `False` |
| [validate_prompt_text(text, max_length)](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#51-66) | Strips, checks not empty, checks length; raises `ValueError` |
| [validate_jira_ticket_format(ticket)](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#68-82) | Regex check + uppercase normalisation; raises `ValueError` |
| [validate_environment(env)](file:///d:/Testing%20automation%20frontend/backend/app/utils/validators.py#84-94) | Checks against `{staging, qa, production}`; raises `ValueError` |

---

## `tests/` — Test Suite Stubs

### [tests/api/test_prompt_routes.py](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py)
Route-level integration tests using `httpx.AsyncClient` with a mocked [PromptService](file:///d:/Testing%20automation%20frontend/backend/app/services/prompt_service.py#22-100).

- **[TestParsePrompt](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#18-36)**: valid prompt, Jira extraction, Confluence URL extraction, empty input (422), oversized input (422)
- **[TestGenerateTestCases](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#38-52)**: successful task_id return, Confluence URL in payload, unauthenticated request (401)
- **[TestGetGenerationStatus](file:///d:/Testing%20automation%20frontend/backend/tests/api/test_prompt_routes.py#54-68)**: pending task, unknown task_id (404), completed task (progress=100)

### [tests/services/test_testcase_service.py](file:///d:/Testing%20automation%20frontend/backend/tests/services/test_testcase_service.py)
Pure unit tests using `pytest-asyncio` and `unittest.mock.AsyncMock` to mock [TestCaseRepository](file:///d:/Testing%20automation%20frontend/backend/app/repositories/testcase_repo.py#18-115).

- **[TestListTestCases](file:///d:/Testing%20automation%20frontend/backend/tests/services/test_testcase_service.py#19-37)**: pagination, status filter, search filter, empty result
- **[TestUpdateStatus](file:///d:/Testing%20automation%20frontend/backend/tests/services/test_testcase_service.py#39-57)**: all allowed/disallowed transitions
- **[TestBulkApprove](file:///d:/Testing%20automation%20frontend/backend/tests/services/test_testcase_service.py#59-69)**: all IDs updated, non-existent IDs silently skipped

### [tests/integration/test_zephyr_integration.py](file:///d:/Testing%20automation%20frontend/backend/tests/integration/test_zephyr_integration.py)
Integration tests marked `@pytest.mark.integration` — run against a real staging Zephyr environment. Skipped in normal CI unless `ZEPHYR_API_TOKEN` is set.

- Connection check (valid + invalid credentials)
- Test case creation (returns Zephyr ID)
- Bulk push with rate-limit handling

---

## Data Flow Summary

```
User submits prompt
    │
    ▼
prompt_routes.py → PromptService.parse_prompt()
                              │
                    PromptParser extracts Jira tickets, Confluence URLs
                              │
                    ConfluenceClient + JiraClient fetch external content
                              │
                    PromptService.trigger_generation()
                              │
              ┌───────────────▼────────────────────────────────┐
              │  Celery Task Chain (generation queue)           │
              │  parse_and_enrich → generate_testcases          │
              │  → generate_bdd → generate_selenium             │
              │                                                 │
              │  RequirementAgent → TestCaseAgent               │
              │  → BDDAgent (concurrent) → SeleniumAgent        │
              │                                                 │
              │  Persist to PostgreSQL + index in ChromaDB      │
              └────────────────────────────────────────────────┘
                              │
                    Review/Approval (testcase_routes)
                              │
                    ZephyrService.push_test_cases()
                    → ZephyrClient (with retry)
                    → Update sync_status + zephyr_id in DB
                              │
                    ExecutionService.trigger_execution()
                    → HarnessClient.trigger_pipeline()
                    → Celery: run_harness_pipeline_task (execution queue)
                       polls Harness → streams logs → saves results
                       → generate_ai_insights_task per failure
                              │
                    Results available at /execution/{id}/results
```
