from .database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, TIMESTAMP, CheckConstraint, func, Enum
from sqlalchemy.orm import relationship

import datetime


class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


class OrderStatus(Base):
    __tablename__ = "order_statuses"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), unique=True, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_category_id = Column(
        Integer,
        ForeignKey("vehicle_categories.id"),
        nullable=True)
    customer_name = Column(String(255), nullable=False)
    product_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    status_id = Column(
        Integer,
        ForeignKey("order_statuses.id"),
        nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vehicle_category = relationship("VehicleCategory")
    status = relationship("OrderStatus")

    __table_args__ = (
        CheckConstraint(
            "price > 0",
            name="check_price_positive"),
    )
