from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Order
from ..schemas import OrderCreate, OrderResponse
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}")
def update_order(order_id: int, order: OrderCreate,
                 db: Session = Depends(get_db)):
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order.dict().items():
        setattr(existing_order, key, value)

    db.commit()
    db.refresh(existing_order)
    return existing_order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
