from app.database import engine, SessionLocal
from app.models import Base, OrderStatus, VehicleCategory, Order
from sqlalchemy.exc import IntegrityError, OperationalError
import time
import logging
from datetime import datetime
import os
import random


def init_db(force_recreate=False):
    max_retries = 30
    retry_interval = 1  # seconds

    for attempt in range(max_retries):
        try:
            if force_recreate:
                # Drop all tables first
                Base.metadata.drop_all(bind=engine)

            # Create all tables
            Base.metadata.create_all(bind=engine)

            db = SessionLocal()
            try:
                # Check if we already have data
                if db.query(OrderStatus).count() == 0:
                    # Initialize order statuses
                    statuses = [
                        OrderStatus(status="Nové"),
                        OrderStatus(status="Vybavené"),
                        OrderStatus(status="Vybavuje sa"),
                        OrderStatus(status="Stornované")
                    ]
                    for status in statuses:
                        db.add(status)
                    db.commit()

                    # Initialize vehicle categories
                    categories = [
                        VehicleCategory(name="LKW"),
                        VehicleCategory(name="PKW")
                    ]
                    for category in categories:
                        db.add(category)
                    db.commit()

                    # Get status and category IDs
                    status_map = {
                        status.status: status.id for status in db.query(OrderStatus).all()}
                    category_map = {
                        category.name: category.id for category in db.query(VehicleCategory).all()}

                    # Sample car brands
                    car_brands = [
                        "Mercedes-Benz", "BMW", "Audi", "Volkswagen", "Toyota",
                        "Honda", "Ford", "Renault", "Škoda", "Volvo"
                    ]

                    # Create sample orders for each user
                    for user_id in range(1, 6):  # 5 users
                        # Create 10 orders per user (total 50 orders)
                        for _ in range(10):
                            order = Order(
                                brand=random.choice(car_brands),
                                price=random.uniform(0, 10000),
                                vehicle_category_id=random.randint(1, 2),
                                # Random status from 1 to 4
                                status_id=random.randint(1, 4)
                            )
                            db.add(order)
                        db.commit()

                    print("Database initialized successfully with sample data!")
                else:
                    print("Database already contains data, skipping initialization.")

                return

            except IntegrityError as e:
                print(f"Error initializing database: {e}")
                db.rollback()
            finally:
                db.close()

        except OperationalError as e:
            if attempt < max_retries - 1:
                print(
                    f"Database not ready, retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                print("Max retries reached. Could not connect to the database.")
                raise


if __name__ == "__main__":
    # Use environment variable to control whether to force recreate tables
    force_recreate = os.getenv("FORCE_RECREATE_DB", "false").lower() == "true"
    init_db(force_recreate)
