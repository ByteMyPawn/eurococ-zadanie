from fastapi.testclient import TestClient
from app.main import app
import pytest

# Create test client
client = TestClient(app)


def test_get_categories(client, db_session):
    response = client.get("/api/vehicle-categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("id" in category and "name" in category for category in data)


def test_get_statuses(client, db_session):
    response = client.get("/api/statuses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert all(isinstance(status, str) for status in data.values())
