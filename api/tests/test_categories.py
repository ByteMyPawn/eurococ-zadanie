import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_models import VehicleCategory
import uuid

# Create test client
client = TestClient(app)


def test_get_categories_not_empty(db_session):
    response = client.get("/api/vehicle-categories/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_category(db_session):
    # Use a unique name to avoid conflicts with existing categories
    unique_name = f"Test Category {uuid.uuid4()}"
    response = client.post(
        "/api/vehicle-categories/",
        json={
            "name": unique_name})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == unique_name
    assert "id" in data


def test_create_duplicate_category(db_session):
    # Use a unique name for the first category
    unique_name = f"Test Category {uuid.uuid4()}"
    # Create first category
    client.post("/api/vehicle-categories/", json={"name": unique_name})
    # Try to create duplicate
    response = client.post(
        "/api/vehicle-categories/",
        json={
            "name": unique_name})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_delete_category(db_session):
    # Create a category with a unique name
    unique_name = f"Test Category {uuid.uuid4()}"
    create_response = client.post(
        "/api/vehicle-categories/",
        json={"name": unique_name})
    category_id = create_response.json()["id"]

    # Delete the category
    response = client.delete(f"/api/vehicle-categories/{category_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get("/api/vehicle-categories/")
    assert len([cat for cat in get_response.json()
               if cat["id"] == category_id]) == 0


def test_delete_nonexistent_category(db_session):
    response = client.delete("/api/vehicle-categories/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
