from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_dashaboard_data(db: Session):

    today = date.today()

    total_guests = db.query(models.Guest).count()

    active_rooms = db.query(models.Room).filter(
        models.Room.is_active == True
    ).count()

    active_reservations = db.query(models.Reservation).filter(
        models.Reservation.status == "CONFIRMED"
    ).count()

    monthly_revenue = db.query(
        func.coalesce(func.sum(models.Payment.amount), 0)
    ).filter(
        models.Payment.status == "PAID"
    ).scalar()

    reservations = (
        db.query(models.Reservation)
        .order_by(models.Reservation.id.desc())
        .limit(5)
        .all()
    )

    recent_reservations = []

    for reservation in reservations:

        guest = db.query(models.Guest).filter(
            models.Guest.id == reservation.guest_id
        ).first()

        room = db.query(models.Room).filter(
            models.Room.id == reservation.room_id
        ).first()

        recent_reservations.append(
            {
                "guest": guest.name,
                "room": room.name,
                "check_in": reservation.check_in,
                "check_out": reservation.check_out
            }
        )

    return {
        "total_guests": total_guests,
        "active_rooms": active_rooms,
        "active_reservations": active_reservations,
        "monthly_revenue": float(monthly_revenue),
        "recent_reservations": recent_reservations
    }