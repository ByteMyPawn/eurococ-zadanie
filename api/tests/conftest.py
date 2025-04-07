import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine as prod_engine
from app.models import OrderStatus, VehicleCategory
import os

# Use test database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db:3306/orders_test_db?charset=utf8mb4"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def init_test_data(session):
    # Initialize order statuses
    statuses = [
        OrderStatus(status="Nové"),
        OrderStatus(status="Vybavené"),
        OrderStatus(status="Vybavuje sa"),
        OrderStatus(status="Stornované")
    ]
    for status in statuses:
        session.add(status)

    # Initialize vehicle categories
    categories = [
        VehicleCategory(name="LKW"),
        VehicleCategory(name="PKW")
    ]
    for category in categories:
        session.add(category)

    session.commit()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create test database tables
    Base.metadata.create_all(bind=test_engine)

    # Initialize test data
    session = TestingSessionLocal()
    try:
        init_test_data(session)
    finally:
        session.close()

    yield
    # Clean up after all tests are done
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def clean_database():
    # Clean up before each test
    session = TestingSessionLocal()
    try:
        # Don't delete statuses and categories
        tables_to_clean = [table for table in reversed(Base.metadata.sorted_tables)
                           if table.name not in ['order_statuses', 'vehicle_categories']]
        for table in tables_to_clean:
            session.execute(table.delete())
        session.commit()
    finally:
        session.close()
    yield


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
