from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_order():
    response = client.post(
        "/orders/",
        json={
            "customer_name": "Test",
            "price": 10.5,
            "status": "pending"})
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Test"
