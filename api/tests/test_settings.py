from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.models import VehicleCategory, OrderStatus
import pytest

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
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    # Add test data
    test_category = VehicleCategory(name="Test Category")
    test_status = OrderStatus(name="Test Status")
    session.add(test_category)
    session.add(test_status)
    session.commit()

    yield session

    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_get_categories(db_session):
    response = client.get("/api/settings/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Test Category" in data.values()


def test_create_category(db_session):
    response = client.post(
        "/api/settings/categories",
        json={"name": "New Category"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Category"
    assert "id" in data


def test_create_category_empty_name(db_session):
    response = client.post(
        "/api/settings/categories",
        json={"name": ""}
    )
    assert response.status_code == 422  # Validation error


def test_delete_category(db_session):
    # First get the category ID
    get_response = client.get("/api/settings/categories")
    categories = get_response.json()
    category_id = next(id for id, name in categories.items()
                       if name == "Test Category")

    # Then delete it
    response = client.delete(f"/api/settings/categories/{category_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get("/api/settings/categories")
    categories = get_response.json()
    assert "Test Category" not in categories.values()


def test_delete_nonexistent_category(db_session):
    response = client.delete("/api/settings/categories/999")
    assert response.status_code == 404


def test_get_statuses(db_session):
    response = client.get("/api/settings/statuses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Test Status" in data.values()


def test_create_status(db_session):
    response = client.post(
        "/api/settings/statuses",
        json={"name": "New Status"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Status"
    assert "id" in data


def test_create_status_empty_name(db_session):
    response = client.post(
        "/api/settings/statuses",
        json={"name": ""}
    )
    assert response.status_code == 422  # Validation error


def test_delete_status(db_session):
    # First get the status ID
    get_response = client.get("/api/settings/statuses")
    statuses = get_response.json()
    status_id = next(id for id, name in statuses.items()
                     if name == "Test Status")

    # Then delete it
    response = client.delete(f"/api/settings/statuses/{status_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get("/api/settings/statuses")
    statuses = get_response.json()
    assert "Test Status" not in statuses.values()


def test_delete_nonexistent_status(db_session):
    response = client.delete("/api/settings/statuses/999")
    assert response.status_code == 404
