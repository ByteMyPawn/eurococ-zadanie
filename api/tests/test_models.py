from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(
            50,
            collation='utf8mb4_unicode_ci'),
        unique=True,
        nullable=False)


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        String(
            50,
            collation='utf8mb4_unicode_ci'),
        unique=True,
        nullable=False)
    orders = relationship("Order", back_populates="status")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_category_id = Column(
        Integer,
        ForeignKey("vehicle_categories.id"),
        nullable=True)
    brand = Column(String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    price = Column(Float, nullable=False)
    status_id = Column(
        Integer,
        ForeignKey("order_statuses.id"),
        nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle_category = relationship("VehicleCategory")
    status = relationship("OrderStatus")
