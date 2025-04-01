from app.database import engine, SessionLocal
from app.models import Base, OrderStatus, VehicleCategory
from sqlalchemy.exc import IntegrityError, OperationalError
import time
import logging


def init_db():
    max_retries = 30
    retry_interval = 1  # seconds

    for attempt in range(max_retries):
        try:
            # Drop all tables first
            Base.metadata.drop_all(bind=engine)
            # Create all tables
            Base.metadata.create_all(bind=engine)

            db = SessionLocal()
            try:
                # Initialize order statuses
                statuses = [
                    OrderStatus(status="Nová"),
                    OrderStatus(status="Spracováva sa"),
                    OrderStatus(status="Dokončená"),
                    OrderStatus(status="Zrušená")
                ]
                db.bulk_save_objects(statuses)

                # Initialize vehicle categories
                categories = [
                    VehicleCategory(name="Osobné auto"),
                    VehicleCategory(name="Nákladné auto"),
                    VehicleCategory(name="Motocykel"),
                    VehicleCategory(name="Autobus")
                ]
                db.bulk_save_objects(categories)

                db.commit()
                print("Database initialized successfully!")
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
    init_db()
