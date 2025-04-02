from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from ..database import SessionLocal
from ..models import Order
from ..schemas import OrderCreate, OrderResponse
from typing import List, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

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


class PaginatedResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


@router.get("/", response_model=PaginatedResponse)
def get_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    price_from: Optional[str] = None,
    price_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching orders - page: {page}, per_page: {per_page}")

    # Build query
    query = db.query(Order)

    # Apply filters
    if search and search.strip():
        query = query.filter(Order.brand.ilike(f"%{search.strip()}%"))

    if status and status.strip():
        try:
            status_id = int(status)
            query = query.filter(Order.status_id == status_id)
        except ValueError:
            pass

    if category and category.strip():
        try:
            category_id = int(category)
            query = query.filter(Order.vehicle_category_id == category_id)
        except ValueError:
            pass

    if date_from and date_from.strip():
        try:
            date_from_dt = datetime.fromisoformat(date_from)
            query = query.filter(Order.created_at >= date_from_dt)
        except ValueError:
            pass

    if date_to and date_to.strip():
        try:
            date_to_dt = datetime.fromisoformat(date_to)
            query = query.filter(Order.created_at <= date_to_dt)
        except ValueError:
            pass

    if price_from and price_from.strip():
        try:
            price_from_val = float(price_from)
            query = query.filter(Order.price >= price_from_val)
        except ValueError:
            pass

    if price_to and price_to.strip():
        try:
            price_to_val = float(price_to)
            query = query.filter(Order.price <= price_to_val)
        except ValueError:
            pass

    # Get total count
    total = query.count()
    logger.info(f"Total orders in database: {total}")

    total_pages = (total + per_page - 1) // per_page
    logger.info(f"Total pages: {total_pages}")

    # Get paginated orders
    orders = query\
        .order_by(desc(Order.id))\
        .offset((page - 1) * per_page)\
        .limit(per_page)\
        .all()

    logger.info(f"Retrieved {len(orders)} orders")
    for order in orders:
        logger.info(
            f"Order: id={order.id}, brand={order.brand}, category_id={order.vehicle_category_id}, status_id={order.status_id}")

    # Convert orders to response format
    order_responses = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "brand": order.brand,
            "price": order.price,
            "created_at": order.created_at,
            "vehicle_category_id": order.vehicle_category_id,
            "status_id": order.status_id
        }
        order_responses.append(order_dict)

    return {
        "items": order_responses,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }


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
