from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import VehicleCategory

router = APIRouter(
    prefix="/vehicle-categories",
    tags=["vehicles"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(VehicleCategory).all()
    return {"categories": [{"id": cat.id, "name": cat.name}
                           for cat in categories]}
