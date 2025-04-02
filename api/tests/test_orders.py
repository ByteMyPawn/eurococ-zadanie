from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from app.models import Order, OrderStatus, VehicleCategory
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = Session(engine)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_get_orders(db):
    # Create test data
    status = OrderStatus(status="Nové")
    category = VehicleCategory(name="PKW")
    db.add(status)
    db.add(category)
    db.commit()

    order = Order(
        brand="Test Brand",
        price=1000.0,
        vehicle_category_id=category.id,
        status_id=status.id
    )
    db.add(order)
    db.commit()

    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["brand"] == "Test Brand"


def test_create_order(db):
    # Create test data
    status = OrderStatus(status="Nové")
    category = VehicleCategory(name="PKW")
    db.add(status)
    db.add(category)
    db.commit()

    order_data = {
        "brand": "New Brand",
        "price": 2000.0,
        "vehicle_category_id": category.id,
        "status_id": status.id
    }

    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "New Brand"
    assert data["price"] == 2000.0


def test_create_order_negative_price(db):
    # Create test data
    status = OrderStatus(status="Nové")
    category = VehicleCategory(name="PKW")
    db.add(status)
    db.add(category)
    db.commit()

    order_data = {
        "brand": "New Brand",
        "price": -100.0,  # Negative price
        "vehicle_category_id": category.id,
        "status_id": status.id
    }

    response = client.post("/orders", json=order_data)
    assert response.status_code == 422  # Validation error


def test_update_order(db):
    # Create test data
    status = OrderStatus(status="Nové")
    category = VehicleCategory(name="PKW")
    db.add(status)
    db.add(category)
    db.commit()

    order = Order(
        brand="Test Brand",
        price=1000.0,
        vehicle_category_id=category.id,
        status_id=status.id
    )
    db.add(order)
    db.commit()

    update_data = {
        "brand": "Updated Brand",
        "price": 1500.0,
        "vehicle_category_id": category.id,
        "status_id": status.id
    }

    response = client.put(f"/orders/{order.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "Updated Brand"
    assert data["price"] == 1500.0


def test_delete_order(db):
    # Create test data
    status = OrderStatus(status="Nové")
    category = VehicleCategory(name="PKW")
    db.add(status)
    db.add(category)
    db.commit()

    order = Order(
        brand="Test Brand",
        price=1000.0,
        vehicle_category_id=category.id,
        status_id=status.id
    )
    db.add(order)
    db.commit()

    response = client.delete(f"/orders/{order.id}")
    assert response.status_code == 200

    # Verify order is deleted
    response = client.get(f"/orders/{order.id}")
    assert response.status_code == 404
