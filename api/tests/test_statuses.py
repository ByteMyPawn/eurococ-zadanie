import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


def test_get_statuses_empty(client, db_session):
    response = client.get("/api/statuses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert all(isinstance(status, str) for status in data.values())
