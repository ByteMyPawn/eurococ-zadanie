from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL format for MySQL:
# mysql+mysqlconnector://username:password@host:port/database_name
DATABASE_URL = "mysql+mysqlconnector://root:root@project-db-1:3306/orders_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # This will show SQL queries in logs
)

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
