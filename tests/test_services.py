import asyncio
from unittest.mock import patch
import pytest
from app.models import PlanRequest
from app.services import RepositoryInputError, create_plan, deterministic_plan, parse_github_url

def test_parse_github_repository_url():
    assert parse_github_url("https://github.com/fastapi/fastapi") == ("fastapi", "fastapi")
    assert parse_github_url("https://github.com/fastapi/fastapi.git") == ("fastapi", "fastapi")

@pytest.mark.parametrize("url", ["http://github.com/owner/repo", "https://evil.example/owner/repo", "https://github.com/owner/repo/tree/main", "https://github.com/owner"])
def test_reject_unsupported_repository_urls(url):
    with pytest.raises(RepositoryInputError):
        parse_github_url(url)

def test_deterministic_plan_has_verification_and_criteria():
    plan = deterministic_plan(PlanRequest(task="Add API key authentication to my service"))
    assert plan.generated_by == "deterministic"
    assert any(step.category == "test" for step in plan.steps)
    assert plan.acceptance_criteria
    assert "No repository changes" in plan.summary

def test_devops_task_includes_operational_readiness():
    plan = deterministic_plan(PlanRequest(task="Prepare CI/CD pipeline for production deployment"))
    assert any(step.category == "operate" for step in plan.steps)

def test_create_plan_falls_back_without_provider_key():
    with patch("app.services.get_settings") as settings:
        settings.return_value.openrouter_api_key = None
        plan = asyncio.run(create_plan(PlanRequest(task="Add caching to the API response layer")))
    assert plan.generated_by == "deterministic"
