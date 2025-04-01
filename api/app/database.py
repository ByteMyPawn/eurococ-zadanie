from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Using DATABASE_URL: {DATABASE_URL}")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

# Set UTF8MB4 for all connections


@event.listens_for(engine, 'connect')
def set_utf8mb4(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
    finally:
        cursor.close()


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
