from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Order schemas


class OrderBase(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    product_name: str = Field(..., example="Laptop")
    price: float = Field(..., gt=0, example=999.99)


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
    created_at: datetime

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
