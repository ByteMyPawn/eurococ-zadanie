from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import OrderStatus
from ..schemas import OrderStatusCreate, OrderStatusResponse
from typing import List

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


@router.get("/statuses", response_model=List[OrderStatusResponse])
def get_statuses(db: Session = Depends(get_db)):
    statuses = db.query(OrderStatus).all()
    return statuses


@router.post("/statuses", response_model=OrderStatusResponse)
def create_status(status: OrderStatusCreate, db: Session = Depends(get_db)):
    db_status = OrderStatus(status=status.status)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


@router.delete("/statuses/{status_id}")
def delete_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(OrderStatus).filter(
        OrderStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(status)
    db.commit()
    return {"message": "Status deleted successfully"}
