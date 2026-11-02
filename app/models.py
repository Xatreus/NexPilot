"""Typed API request and response models."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "NexPilot"
    version: str = "0.1.0"

class PlanRequest(BaseModel):
    task: str = Field(min_length=8, max_length=4000)
    repository_url: HttpUrl | None = None
    context: str | None = Field(default=None, max_length=8000)

class PlanStep(BaseModel):
    title: str
    details: str
    category: Literal["inspect", "design", "implement", "test", "deliver", "operate"]

class EngineeringPlan(BaseModel):
    title: str
    summary: str
    assumptions: list[str] = Field(default_factory=list)
    steps: list[PlanStep]
    risks: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    generated_by: Literal["deterministic", "openrouter"] = "deterministic"

class RepositoryInspectRequest(BaseModel):
    repository_url: HttpUrl

class RepositoryFinding(BaseModel):
    category: str
    status: Literal["present", "missing"]
    evidence: str
    recommendation: str

class RepositoryReport(BaseModel):
    repository: str
    description: str | None = None
    default_branch: str | None = None
    stars: int = 0
    language: str | None = None
    findings: list[RepositoryFinding]
    inspected_at: datetime
    limitations: list[str] = Field(default_factory=list)

class InspectionRecord(BaseModel):
    id: int
    kind: str
    subject: str
    created_at: datetime
    model_config = {"from_attributes": True}
