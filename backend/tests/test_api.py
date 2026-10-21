import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

from backend.main import app
from backend.database import Base, get_db
from backend.models.database import Line, Station, DelayRecord

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    line = Line(id="central", name="Central Line")
    db.add(line)
    station = Station(line_id="central", name="Dadar", display_order=1)
    db.add(station)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_create_and_get_delay():
    payload = {
        "line": "central",
        "station": "Dadar",
        "delay_minutes": 15,
        "direction": "up",
        "notes": "Signal failure"
    }
    response = client.post("/api/v2/delays", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    
    get_res = client.get("/api/v2/delays?line=central")
    assert get_res.status_code == 200
    listing = get_res.json()
    assert listing["count"] == 1
    assert listing["delays"][0]["station"] == "Dadar"
    assert listing["delays"][0]["delay_minutes"] == 15
