
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .database import SessionLocal, engine, Base
import os
from .models import Order, VehicleCategory, OrderStatus

app = FastAPI()

# Create tables


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")


# Call init_db when starting the application
init_db()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    product_name: str = Field(..., example="Laptop")
    # Zabezpečenie, že cena nebude záporná
    price: float = Field(..., gt=0, example=999.99)

# Získanie všetkých objednávok


@app.get("/orders")
def get_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders

# Vytvorenie novej objednávky


@app.post("/orders")
def create_order(order: OrderCreate):
    db = SessionLocal()
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()
    return new_order

# Získanie jednej objednávky podľa ID


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    db.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Aktualizácia objednávky


@app.put("/orders/{order_id}")
def update_order(order_id: int, order: OrderCreate):
    db = SessionLocal()
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")

    existing_order.customer_name = order.customer_name
    existing_order.product_name = order.product_name
    existing_order.price = order.price

    db.commit()
    db.refresh(existing_order)
    db.close()
    return existing_order

# Vymazanie objednávky


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    db.close()
    return {"message": "Order deleted successfully"}
