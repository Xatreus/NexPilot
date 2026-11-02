from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_dashboard_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "NexPilot" in response.text
    assert "Engineering planner" in response.text

def test_plan_endpoint_uses_deterministic_fallback(monkeypatch):
    from app import services
    monkeypatch.setattr(services, "get_settings", lambda: type("Settings", (), {"openrouter_api_key": None})())
    response = client.post("/api/v1/plans", json={"task": "Add request validation to the API"})
    assert response.status_code == 200
    assert response.json()["generated_by"] == "deterministic"

def test_plan_rejects_short_task():
    response = client.post("/api/v1/plans", json={"task": "fix"})
    assert response.status_code == 422
