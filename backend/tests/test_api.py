import os
os.environ["DATABASE_URL"] = "sqlite:///./test_delay_tracker.db"
from fastapi.testclient import TestClient
from backend.database import Base, engine
from backend.main import app

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_create_and_list_delay():
    payload = {"line": "central", "station": "Dadar", "direction": "UP", "delay_minutes": 8}
    created = client.post("/api/v2/delays", json=payload)
    assert created.status_code == 201
    assert created.json()["severity"] == "minor"
    assert client.get("/api/v2/delays?line=central").status_code == 200
