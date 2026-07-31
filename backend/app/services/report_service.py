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

    monthly_revenue = db.query(models.Reservation).filter(
        models.Reservation.total_price == "PAID",
        
    )