from fastapi import FastAPI
from .database import engine, Base
from .models import Order, VehicleCategory, OrderStatus, Base
from .routes import orders, vehicles, health
from fastapi.middleware.cors import CORSMiddleware
from init_db import init_db
from app.models import Base
from sqlalchemy import text


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")

        # Initialize database with default data
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error during startup: {e}")
        raise


# Add CORS middleware to allow requests from your Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)
app.include_router(vehicles.router)
app.include_router(health.router)


# Test endpoint
@app.get("/")
def read_root():
    return {"message": "API is working!"}


@app.get("/test-db")
async def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}
