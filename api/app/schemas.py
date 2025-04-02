from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Order schemas


class OrderBase(BaseModel):
    brand: str = Field(..., example="Mercedes")
    price: float = Field(..., ge=0, example=999.99)
    vehicle_category_id: Optional[int] = None
    status_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    vehicle_category_id: Optional[int] = None
    status_id: Optional[int] = None

    class Config:
        orm_mode = True  # Allows the Pydantic model to read data from ORM objects

# Vehicle category schemas


class VehicleCategoryBase(BaseModel):
    name: str = Field(..., example="Car")


class VehicleCategoryCreate(VehicleCategoryBase):
    pass


class VehicleCategoryResponse(VehicleCategoryBase):
    id: int

    class Config:
        orm_mode = True

# Order status schemas


class OrderStatusBase(BaseModel):
    status: str = Field(..., example="Vybavene")


class OrderStatusCreate(OrderStatusBase):
    pass


class OrderStatusResponse(OrderStatusBase):
    id: int

    class Config:
        orm_mode = True
