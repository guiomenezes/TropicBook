from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_dashaboard_data(db: Session):

    today = date.today()

    active_reservations = db.query(models.Reservation).filter(
        models.Reservation.status == 'CONFIRMED').count()

    occupied_rooms = db.query(models.Reservation).filter(
        models.Reservation.status == 'CONFIRMED',
        models.Reservation.check_in <= today, 
        models.Reservation.check_out > today
    ).count()

    today_checkins = db.query(models.Reservation).filter(
        models.Reservation.check_in == today,
        models.Reservation.status == "CONFIRMED"
    ).count()

    today_checkouts = db.query(models.Reservation).filter(
        models.Reservation.check_out == today,
        models.Reservation.status == "CONFIRMED"
    ).count()

    monthly_revenue = db.query(func.coalesce(func.sum(models.Payment.amount), 0)).filter(
        models.Payment.status == 'PAID'
    ).scalar()

    latest_reservations = (
        db.query(models.Reservation).order_by(models.Reservation.id.desc()).limit(5).all()
    )

    return {
        'active_reservations': active_reservations,
        'ocuppied_rooms': occupied_rooms,
        'today_checkins': today_checkins,
        'today_checkouts': today_checkouts,
        'monthly_revenue': monthly_revenue,
        'latest_reservations': latest_reservations
    }