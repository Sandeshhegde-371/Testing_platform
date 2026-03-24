# AI-Powered Test Case Lifecycle Platform — Backend

Production-ready Python/FastAPI backend scaffold for the full AI-driven test lifecycle:

**Prompt → AI Generation → BDD/Selenium → Zephyr Sync → Harness Execution → Results**

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI + Uvicorn |
| Database | PostgreSQL 16 + SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Cache / Queue | Redis 7 |
| Async tasks | Celery 5 + Flower |
| AI / LLM | LangChain + Google Gemini |
| Vector Store | ChromaDB (RAG) |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) |

---

## Folder Structure

```
backend/
├── app/
│   ├── api/v1/routes/     # HTTP route handlers
│   ├── core/              # Config, security, logging
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── services/          # Business logic (pluggable)
│   ├── repositories/      # DB access layer
│   ├── integrations/      # Jira, Confluence, Zephyr, Harness clients
│   ├── ai/                # LLM agents, prompts, RAG
│   ├── tasks/             # Celery async workers
│   ├── utils/             # Shared helpers
│   └── main.py            # FastAPI app entry point
├── tests/
├── scripts/
├── alembic/
├── Dockerfile
└── docker-compose.yml
```

---

## Quick Start

```bash
# 1. Copy env file
cp .env.example .env
# Fill in your API keys

# 2. Start all services
docker compose up -d

# 3. Run migrations
./scripts/migrate.sh

# 4. API docs
open http://localhost:8000/docs
```

---

## Individual Scripts

```bash
./scripts/start.sh    # Start API server
./scripts/worker.sh   # Start Celery worker
./scripts/migrate.sh  # Run Alembic migrations
```

---

## API Endpoints (planned)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/prompt/generate` | Trigger AI test case generation |
| `GET` | `/api/v1/testcases/` | List all test cases |
| `PATCH` | `/api/v1/testcases/{id}/approve` | Approve a test case |
| `POST` | `/api/v1/zephyr/push` | Push test cases to Zephyr |
| `POST` | `/api/v1/execution/run` | Trigger Harness pipeline |
| `GET` | `/api/v1/execution/{id}/results` | Fetch execution results |
| `GET` | `/api/v1/health` | Health check |

---

## Architecture Layers

1. **API Layer** — FastAPI route handlers, request validation, response formatting
2. **Service Layer** — Business logic, orchestration (plug your logic here)
3. **Repository Layer** — DB queries via SQLAlchemy (swap DB without changing services)
4. **Integration Layer** — HTTP clients for Jira, Confluence, Zephyr, Harness
5. **AI Layer** — LangChain agents + RAG pipeline for test case generation
6. **Task Layer** — Celery workers for long-running async operations
