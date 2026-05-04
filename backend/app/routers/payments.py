from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.auth.roles import require_role
from app.auth.deps import get_current_user
from app.services import payment_service

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post('/', response_model=schemas.PaymentResponse)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))
):
    return payment_service.create_payment(db, payment)


@router.get('/', response_model=list[schemas.PaymentResponse])
def list_payments(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return payment_service.get_payments(db)


@router.get('/{payment_id}', response_model=schemas.PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    payment = payment_service.get_payment_by_id(db, payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@router.delete('/{payment_id}')
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN']))
):
    result = payment_service.delete_payment(db, payment_id)

    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")

    return {"message": "Deleted successfully"}