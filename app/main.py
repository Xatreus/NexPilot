"""NexPilot web application."""
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api import router
from app.config import get_settings
from app.db import init_db

STATIC_DIR = Path(__file__).parent / "static"

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

settings = get_settings()
app = FastAPI(title=settings.app_name, summary="An AI software engineering and DevOps assistant.", description="Plan engineering work, inspect public GitHub repositories, and track recent activity. Model-powered planning is optional.", version="0.1.0", lifespan=lifespan)
app.include_router(router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))
