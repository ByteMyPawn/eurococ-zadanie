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


@router.get("", response_model=PaginatedResponse)
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
    logger.info(
        f"Filters - date_from: {date_from}, date_to: {date_to}, price_from: {price_from}, price_to: {price_to}")

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
            logger.warning(f"Invalid status ID format: {status}")

    if category and category.strip():
        try:
            category_id = int(category)
            query = query.filter(Order.vehicle_category_id == category_id)
        except ValueError:
            logger.warning(f"Invalid category ID format: {category}")

    if date_from and date_from.strip():
        try:
            # Try parsing with time first
            date_from_dt = datetime.fromisoformat(date_from)
        except ValueError:
            try:
                # If that fails, try parsing just the date
                date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
            except ValueError:
                logger.warning(f"Invalid date_from format: {date_from}")
            else:
                query = query.filter(Order.created_at >= date_from_dt)
        else:
            query = query.filter(Order.created_at >= date_from_dt)

    if date_to and date_to.strip():
        try:
            # Try parsing with time first
            date_to_dt = datetime.fromisoformat(date_to)
        except ValueError:
            try:
                # If that fails, try parsing just the date
                date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
            except ValueError:
                logger.warning(f"Invalid date_to format: {date_to}")
            else:
                # Add end of day time (23:59:59) to include the entire day
                date_to_dt = date_to_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Order.created_at <= date_to_dt)
        else:
            query = query.filter(Order.created_at <= date_to_dt)

    if price_from and price_from.strip():
        try:
            # Try to convert to float, handling both comma and dot decimal
            # separators
            price_from_val = float(price_from.replace(',', '.'))
            query = query.filter(Order.price >= price_from_val)
            logger.info(f"Applied price_from filter: {price_from_val}")
        except ValueError:
            logger.warning(f"Invalid price_from format: {price_from}")

    if price_to and price_to.strip():
        try:
            # Try to convert to float, handling both comma and dot decimal
            # separators
            price_to_val = float(price_to.replace(',', '.'))
            query = query.filter(Order.price <= price_to_val)
            logger.info(f"Applied price_to filter: {price_to_val}")
        except ValueError:
            logger.warning(f"Invalid price_to format: {price_to}")

    # Get total count
    total = query.count()
    logger.info(f"Total orders in database: {total}")

    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page
    logger.info(f"Total pages: {total_pages}")

    # Apply pagination
    query = query.order_by(desc(Order.created_at))
    query = query.offset((page - 1) * per_page).limit(per_page)

    # Execute query
    orders = query.all()
    logger.info(f"Retrieved {len(orders)} orders")

    # Log each order for debugging
    for order in orders:
        logger.info(
            f"Order: id={order.id}, brand={order.brand}, category_id={order.vehicle_category_id}, status_id={order.status_id}")

    return {
        "items": orders,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }


@router.post("", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderCreate,
                 db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order.dict().items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
