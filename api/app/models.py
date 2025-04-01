from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, TIMESTAMP, CheckConstraint, func, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime
from .database import Base


class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_slovak_ci'
    }

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50, charset='utf8mb4', collation='utf8mb4_slovak_ci'),
                  unique=True, nullable=False)


class OrderStatus(Base):
    __tablename__ = "order_statuses"
    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_slovak_ci'
    }

    id = Column(Integer, primary_key=True, index=True)
    status = Column(VARCHAR(50, charset='utf8mb4', collation='utf8mb4_slovak_ci'),
                    unique=True, nullable=False)
    orders = relationship("Order", back_populates="status")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
        {
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_slovak_ci'
        }
    )

    id = Column(Integer, primary_key=True, index=True)
    vehicle_category_id = Column(
        Integer,
        ForeignKey("vehicle_categories.id"),
        nullable=True)
    customer_name = Column(VARCHAR(255, charset='utf8mb4', collation='utf8mb4_slovak_ci'),
                           nullable=False)
    product_name = Column(VARCHAR(255, charset='utf8mb4', collation='utf8mb4_slovak_ci'),
                          nullable=False)
    price = Column(Float, nullable=False)
    status_id = Column(
        Integer,
        ForeignKey("order_statuses.id"),
        nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle_category = relationship("VehicleCategory")
    status = relationship("OrderStatus")
