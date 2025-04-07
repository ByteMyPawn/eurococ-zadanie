from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..models import VehicleCategory, Order
from ..schemas import VehicleCategoryCreate, VehicleCategoryResponse
from typing import List

router = APIRouter(
    prefix="/vehicle-categories",
    tags=["vehicles"]
)


@router.get("/", response_model=List[VehicleCategoryResponse])
def get_vehicle_categories(db: Session = Depends(get_db)):
    categories = db.query(VehicleCategory).all()
    return categories


@router.post("/", response_model=VehicleCategoryResponse)
def create_vehicle_category(
        category: VehicleCategoryCreate, db: Session = Depends(get_db)):
    try:
        db_category = VehicleCategory(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle category with name '{category.name}' already exists"
        )


@router.get("/{category_id}",
            response_model=VehicleCategoryResponse)
def get_vehicle_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(VehicleCategory).filter(
        VehicleCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Vehicle category not found")
    return category


@router.put("/{category_id}",
            response_model=VehicleCategoryResponse)
def update_vehicle_category(
        category_id: int, category: VehicleCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(VehicleCategory).filter(
        VehicleCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Vehicle category not found")

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}")
def delete_vehicle_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(VehicleCategory).filter(
        VehicleCategory.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Vehicle category not found")

    # Check if category is in use
    orders_using_category = db.query(Order).filter(
        Order.vehicle_category_id == category_id).first()
    if orders_using_category:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category that is in use")

    db.delete(category)
    db.commit()
    return {"message": "Vehicle category deleted successfully"}
