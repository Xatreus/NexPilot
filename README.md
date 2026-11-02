# NexPilot
### AI Software Engineering & DevOps Assistant

**Plan better. Understand codebases. Ship safer.**

NexPilot is an engineering copilot prototype designed to help developers turn software tasks into actionable plans and quickly assess the delivery foundations of public GitHub repositories. It combines structured API contracts, optional model-assisted planning, repository intelligence, a lightweight dashboard, and a CLI.

> **Status:** early prototype. Planning and read-only repository checks are implemented in this branch. Autonomous code edits, shell execution, RAG, private repositories, and live deployment operations are not implemented.

## What it does

- **Engineering planner:** converts a task into a sequence of inspect, design, implement, test, and deliver steps, with risks and acceptance criteria.
- **Optional LLM support:** uses an OpenRouter-compatible chat-completions API when configured; falls back to a deterministic plan when no key is available or the provider fails.
- **Repository intelligence:** checks public GitHub metadata and repository-tree signals for documentation, tests, CI, dependency manifests, container configuration, and a security policy.
- **Activity history:** stores recent planning and repository-inspection events locally.
- **Web dashboard:** a responsive dark-mode command center for the main workflows.
- **CLI:** create an engineering plan from your terminal.
- **Safety-first defaults:** read-only GitHub access; no untrusted code execution; no automatic commits, pushes, or deployments.

## Stack

| Layer | Technology | Purpose |
|---|---|---|
| API | FastAPI | Typed endpoints and OpenAPI docs |
| Validation | Pydantic v2 + Pydantic Settings | Request contracts and environment configuration |
| External APIs | HTTPX + GitHub REST API | Bounded-timeout asynchronous HTTP calls |
| Persistence | SQLAlchemy 2 + SQLite | Local activity history |
| Optional model | OpenRouter-compatible API | Model-assisted planning with fallback |
| CLI | Typer | Terminal workflow |
| UI | HTML, CSS, vanilla JavaScript | Lightweight responsive dashboard |
| Quality | Pytest + Ruff | Tests and linting |
| Runtime | Uvicorn + Docker | Local API runtime and container path |

## Architecture

    Browser dashboard / CLI
              |
              v
           FastAPI
        /      |       \
   Planner  GitHub     History
      |      Inspector    |
  Optional      |      SQLAlchemy
  LLM API    GitHub API  SQLite
      |
  Deterministic fallback

The model provider is optional. Repository inspection checks file paths and metadata only; it does not prove code quality, test success, dependency safety, or deployment health.

## Quick start

Requirements: Python 3.11 or newer.

    git clone https://github.com/Xatreus/NexPilot.git
    cd NexPilot
    python -m venv .venv

Windows PowerShell:

    .venv\Scripts\Activate.ps1

macOS/Linux:

    source .venv/bin/activate

Install and run:

    python -m pip install -r requirements.txt
    uvicorn app.main:app --reload

Open http://127.0.0.1:8000 for the dashboard and http://127.0.0.1:8000/docs for API docs.

## Optional model configuration

Copy .env.example to .env and add your provider key:

    OPENROUTER_API_KEY=your_key_here
    OPENROUTER_MODEL=your_supported_model_id

Without a key, the engineering planner still works using its deterministic fallback. Never commit .env or real credentials.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/v1/health | Service health |
| POST | /api/v1/plans | Generate an engineering plan |
| POST | /api/v1/repositories/inspect | Inspect a public GitHub repository |
| GET | /api/v1/history?limit=10 | Read recent local activity |

Example plan request:

    {
      "task": "Add API key authentication and tests to my FastAPI service"
    }

Example repository request:

    {
      "repository_url": "https://github.com/fastapi/fastapi"
    }

## CLI

    python -m app.cli plan "Add caching to the API response layer"

## Tests and lint

    python -m pytest -q
    ruff check .

## Security boundaries

- Only HTTPS repository URLs hosted on github.com are accepted by the inspector.
- Repository code is not downloaded or executed.
- Model-generated plans are advisory and validated against typed schemas.
- Provider errors fall back to deterministic planning.
- Do not expose the service publicly without authentication, rate limiting, and deployment hardening.
- Never submit secrets or confidential source code.

See SECURITY.md and ARCHITECTURE.md for details.

## Roadmap

1. Repository-aware summaries with bounded file retrieval and evidence paths.
2. Evaluation fixtures for plan quality and repository findings.
3. RAG over selected documentation with source citations and retrieval tests.
4. Approved patch proposals and isolated test execution.
5. Read-only CI failure summaries, then carefully permissioned DevOps integrations.

NexPilot is a prototype and learning project. Each capability will be marked implemented only after code and tests exist.
