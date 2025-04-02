import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.models import OrderStatus

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_get_statuses_empty(db_session):
    response = client.get("/api/statuses")
    assert response.status_code == 200
    assert response.json() == {}


def test_create_status(db_session):
    response = client.post("/api/statuses", json={"name": "Test Status"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Test Status"
    assert "id" in data


def test_create_duplicate_status(db_session):
    # Create first status
    client.post("/api/statuses", json={"name": "Test Status"})
    # Try to create duplicate
    response = client.post("/api/statuses", json={"name": "Test Status"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_delete_status(db_session):
    # Create a status
    create_response = client.post(
        "/api/statuses", json={"name": "Test Status"})
    status_id = create_response.json()["id"]

    # Delete the status
    response = client.delete(f"/api/statuses/{status_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get("/api/statuses")
    assert status_id not in get_response.json()


def test_delete_nonexistent_status(db_session):
    response = client.delete("/api/statuses/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
