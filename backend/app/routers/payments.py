from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models

router = APIRouter(
    prefix='/payments',
    tags=['Payments']
)

@router.post('/', response_model=schemas.PaymentResponse)
def create_payment(payments: schemas.PaymentCreate, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == payments.reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found.')
    
    if payments.amount <= 0:
        raise HTTPException(status_code=400, detail='Amount must greater than zero.')
    
    db_payment = models.Payment(**payments.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment

@router.get('/', response_model=list[schemas.PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    payments = db.query(models.Payment).all()
    return payments

@router.get('/{payment_id}', response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    
    return db_payment

@router.put('/{payment_id}', response_model=schemas.PaymentResponse)
def update_payment(payment_id: int, payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    
    reservation = db.query(models.Reservation).filter(models.Reservation.id == payment.reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found.')
    
    if payment.amount <=0:
        raise HTTPException(status_code=400, detail='Amount must be greater than zero.')
    
    db_payment.reservation_id = payment.reservation_id
    db_payment.amount = payment.amount
    db_payment.payment_method = payment.payment_method
    db_payment.status = payment.status
    
    db.commit()
    db.refresh(db_payment)

    return db_payment

@router.delete('/{payment_id}')
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()

    if not db_payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    
    db.delete(db_payment)
    db.commit()

    return {'message': 'Payment deleted successfully.'}

