# NexPilot Architecture

## Product definition
NexPilot is an AI software engineering and DevOps assistant. It helps developers turn engineering goals into reviewable plans and assess delivery fundamentals in public GitHub repositories. This first vertical slice is read-only and usable without a paid model API.

## Implemented vertical slice
```text
Browser dashboard / CLI -> FastAPI
  -> Engineering planner -> Optional OpenRouter-compatible model / deterministic fallback
  -> GitHub inspector -> GitHub REST API (public metadata + file tree)
  -> Activity history -> SQLAlchemy -> SQLite by default
```

## Stack and purpose
- **FastAPI + Pydantic v2:** typed HTTP contracts and OpenAPI documentation.
- **Pydantic Settings:** environment-driven configuration.
- **HTTPX:** asynchronous external API calls with timeouts.
- **SQLAlchemy 2:** persistence boundary for activity history.
- **OpenRouter-compatible API:** optional model-assisted planning with deterministic fallback.
- **Typer:** CLI entry point sharing the planning service.
- **HTML/CSS/JavaScript:** lightweight responsive dashboard without a frontend build system.
- **Pytest + Ruff:** test and lint foundation.
- **Uvicorn + Docker:** application runtime and container path.

## Safety boundaries
- Repository inspection accepts HTTPS github.com URLs and reads public metadata and tree paths.
- Repository code is not downloaded or executed.
- Model output is validated against typed schemas; provider failures fall back to deterministic planning.
- Planning and inspection do not mutate repositories, run shell commands, or deploy infrastructure.
- Do not expose the service publicly without authentication, rate limiting, and deployment hardening.

## Current limitations
The inspector checks file presence, not code quality, vulnerabilities, test results, or deployment health. Activity storage is local. Private repositories, autonomous patching, sandboxed execution, RAG, CI provider integration, and infrastructure operations are not implemented.

## Next steps
1. Bounded source-file retrieval with evidence references.
2. Evaluation fixtures for plans and repository findings.
3. RAG over selected documentation with citations and retrieval tests.
4. Approved patch proposals and isolated test execution.
5. Read-only CI failure summaries before permissioned DevOps actions.
