from fastapi import FastAPI, HTTPException
from .database import engine, Base
from .models import Base as ModelsBase  # Rename to avoid confusion
from .routes import orders, vehicles, health, settings, statuses
from fastapi.middleware.cors import CORSMiddleware
from init_db import init_db
from sqlalchemy import text
import logging
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Orders API",
    description="API for managing orders and vehicle categories",
    version="1.0.0",
    # Disable automatic trailing slashes
    redirect_slashes=False,
    default_response_class=JSONResponse
)

# Create an API router for all routes
api_router = APIRouter()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    try:
        # Initialize database with optional force recreate
        force_recreate = os.getenv(
            "FORCE_RECREATE_DB",
            "false").lower() == "true"
        init_db(force_recreate)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

# Add CORS middleware to allow requests from your Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers under the API router
api_router.include_router(orders.router)
api_router.include_router(vehicles.router)
api_router.include_router(health.router)
api_router.include_router(settings.router)
api_router.include_router(statuses.router)

# Mount the API router with the /api prefix
app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "API is working!",
        "version": "1.0.0"
    }


@app.get("/test-db")
async def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            return {
                "status": "ok",
                "tables": tables,
                "count": len(tables)
            }
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
