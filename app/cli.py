"""Command-line interface for engineering planning."""
import asyncio
import json
import typer
from app.models import PlanRequest
from app.services import create_plan
app = typer.Typer(help="NexPilot — software engineering and DevOps assistant")

@app.command()
def plan(task: str = typer.Argument(..., help="Engineering task to plan")) -> None:
    """Create a verification-first engineering plan."""
    result = asyncio.run(create_plan(PlanRequest(task=task)))
    typer.echo(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    app()
