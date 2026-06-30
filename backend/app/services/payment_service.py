from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

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

def mark_payment_as_paid(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found.')
    
    if payment.status == 'PAID':
        raise HTTPException(status_code=400, detail='Payment alreay completed.')
    
    payment.status = 'PAID'
    payment.payment_method = 'CREDIT_CARD'

    #Atualizar reserva
    reservation = db.query(models.Reservation).filter(models.Reservation.id == payment.reservation_id).first()

    if reservation:
        reservation.status == 'COMPLETED'

    db.commit()
    db.refresh(payment)

    return payment