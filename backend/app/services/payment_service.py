from sqlalchemy.orm import Session
from app import models, schemas


def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.model_dump())

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_payments(db: Session):
    return db.query(models.Payment).all()


def get_payment_by_id(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def delete_payment(db: Session, payment_id: int):
    db_payment = get_payment_by_id(db, payment_id)

    if not db_payment:
        return None

    db.delete(db_payment)
    db.commit()

    return db_payment