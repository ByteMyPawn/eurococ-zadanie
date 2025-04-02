from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)
