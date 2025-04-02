import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.test_models import Base, VehicleCategory, OrderStatus

# Use existing database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db/project"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


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
