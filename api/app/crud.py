from sqlalchemy.orm import Session
from . import models, schemas


def create_order(db: Session, order: schemas.OrderCreate):
    if order.price < 0:
        raise ValueError("Cena nemôže byť záporná")
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
