"""Versioned HTTP API."""
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from app.db import recent_inspections, record_inspection
from app.models import EngineeringPlan, HealthResponse, InspectionRecord, PlanRequest, RepositoryInspectRequest, RepositoryReport
from app.services import RepositoryInputError, create_plan, inspect_repository

router = APIRouter(prefix="/api/v1")

@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse()

@router.post("/plans", response_model=EngineeringPlan, tags=["engineering"])
async def plan_task(request: PlanRequest) -> EngineeringPlan:
    result = await create_plan(request)
    try:
        record_inspection("plan", request.task)
    except SQLAlchemyError:
        pass
    return result

@router.post("/repositories/inspect", response_model=RepositoryReport, tags=["repository intelligence"])
async def repository_inspection(request: RepositoryInspectRequest) -> RepositoryReport:
    try:
        report = await inspect_repository(str(request.repository_url))
    except RepositoryInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="GitHub inspection failed. Check availability and rate limits.") from exc
    try:
        record_inspection("repository", report.repository)
    except SQLAlchemyError:
        pass
    return report

@router.get("/history", response_model=list[InspectionRecord], tags=["system"])
def inspection_history(limit: int = Query(default=10, ge=1, le=100)) -> list[InspectionRecord]:
    try:
        return recent_inspections(limit)
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Inspection history is temporarily unavailable.") from exc
