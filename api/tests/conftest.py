import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import os

# Use main database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db:3306/orders_db?charset=utf8mb4"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session")
def client():
    # Override the app's database URL for testing
    os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL

    # Override the get_db dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create test client with base URL that includes /api prefix
    with TestClient(app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
def db_session():
    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        # Cleanup - roll back any changes made during the test
        session.rollback()
        session.close()
