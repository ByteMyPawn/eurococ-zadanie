import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from app.models import Order, OrderStatus, VehicleCategory
from sqlalchemy.orm import Session
import time

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = Session(engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_get_orders(client, db_session):
    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    assert "total_pages" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["page"], int)
    assert isinstance(data["per_page"], int)
    assert isinstance(data["total_pages"], int)


def test_create_order(client, db_session):
    # Get an existing status
    status = db_session.query(OrderStatus).first()

    # Create test category with unique name
    timestamp = int(time.time() * 1000)  # Use milliseconds for more uniqueness
    category = VehicleCategory(name=f"Test Category {timestamp}")
    db_session.add(category)
    db_session.commit()

    order_data = {
        "brand": "Test Brand",
        "price": 2000.0,
        "vehicle_category_id": category.id,
        "status_id": status.id
    }

    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "Test Brand"
    assert data["price"] == 2000.0

    # Cleanup - first delete all orders
    db_session.query(Order).delete()
    db_session.commit()

    # Then delete only the category
    db_session.delete(category)
    db_session.commit()


def test_create_order_negative_price(client, db_session):
    # Get an existing status
    status = db_session.query(OrderStatus).first()

    # Create test category with unique name
    timestamp = int(time.time() * 1000 + 1)  # Add 1 to ensure uniqueness
    category = VehicleCategory(name=f"Test Category {timestamp}")
    db_session.add(category)
    db_session.commit()

    order_data = {
        "brand": "Test Brand",
        "price": -100.0,
        "vehicle_category_id": category.id,
        "status_id": status.id
    }

    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0
    assert data["detail"][0]["type"] == "value_error.number.not_ge"
    assert "ensure this value is greater than or equal to 0" in data["detail"][0]["msg"]

    # Cleanup - delete only the category
    db_session.delete(category)
    db_session.commit()


def test_update_order(client, db_session):
    # Get an existing status
    status = db_session.query(OrderStatus).first()

    # Create test category with unique name
    timestamp = int(time.time() * 1000 + 2)  # Add 2 to ensure uniqueness
    category = VehicleCategory(name=f"Test Category {timestamp}")
    db_session.add(category)
    db_session.commit()

    # Create initial order
    order = Order(
        brand="Test Brand",
        price=1000.0,
        vehicle_category_id=category.id,
        status_id=status.id
    )
    db_session.add(order)
    db_session.commit()

    # Use the same category for update
    update_data = {
        "brand": "Updated Brand",
        "price": 1500.0,
        "vehicle_category_id": category.id,  # Use the same category ID
        "status_id": status.id
    }

    response = client.put(f"/api/orders/{order.id}", json=update_data)
    assert response.status_code == 200

    # Verify the update
    updated_order = response.json()
    assert updated_order["brand"] == "Updated Brand"
    assert updated_order["price"] == 1500.0
    assert updated_order["vehicle_category_id"] == category.id
    assert updated_order["status_id"] == status.id

    # Cleanup - first delete all orders
    db_session.query(Order).delete()
    db_session.commit()

    # Then delete only the category
    db_session.delete(category)
    db_session.commit()


def test_delete_order(client, db_session):
    # Get an existing status
    status = db_session.query(OrderStatus).first()

    # Create test category with unique name
    timestamp = int(time.time() * 1000 + 3)  # Add 3 to ensure uniqueness
    category = VehicleCategory(name=f"Test Category {timestamp}")
    db_session.add(category)
    db_session.commit()

    order = Order(
        brand="Test Brand",
        price=1000.0,
        vehicle_category_id=category.id,
        status_id=status.id
    )
    db_session.add(order)
    db_session.commit()

    response = client.delete(f"/api/orders/{order.id}")
    assert response.status_code == 200

    # Cleanup - first delete all orders
    db_session.query(Order).delete()
    db_session.commit()

    # Then delete only the category
    db_session.delete(category)
    db_session.commit()
