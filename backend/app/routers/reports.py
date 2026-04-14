from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models
from app.auth.roles import require_role


router = APIRouter(
    prefix = '/reports',
    tags = ['Reports']
)

@router.get('/summary')
def get_summary(db: Session = Depends(get_db), user= Depends(require_role(['ADMIN']))):
    total_guests = db.query(func.count(models.Guest.id)).scalar()

    total_rooms = db.query(func.count(models.Room.id)).scalar()

    available_rooms = db.query(func.count(models.Room.id)).filter(models.Room.status == 'available').scalar()

    total_reservations = db.query((func.count(models.Reservation.id))).scalar()

    total_revenue = db.query(func.coalesce(func.sum(models.Payment.amount), 0)).filter(models.Payment.status == 'PAID').scalar()

    pending_payments = db.query(func.count(models.Payment.id)).filter(models.Payment.status == 'PENDING').scalar()

    return {
        'total_guest': total_guests,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_reservations': total_reservations,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments
    }