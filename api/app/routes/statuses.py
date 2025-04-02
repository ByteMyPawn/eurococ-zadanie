from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import OrderStatus
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/statuses",
    tags=["statuses"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StatusCreate(BaseModel):
    status: str


class StatusResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True


@router.get("", response_model=Dict[str, str])
def get_statuses(db: Session = Depends(get_db)):
    statuses = db.query(OrderStatus).all()
    status_dict = {str(status.id): status.status for status in statuses}
    return JSONResponse(content=jsonable_encoder(status_dict))


@router.post("", response_model=StatusResponse)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    try:
        new_status = OrderStatus(status=status.status)
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return JSONResponse(content=jsonable_encoder(new_status))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail="Status with this name already exists")


@router.delete("/{status_id}")
def delete_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(OrderStatus).filter(OrderStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    try:
        db.delete(status)
        db.commit()
        return {"message": "Status deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail="Cannot delete status that is in use")
