from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

def room_has_conflict(db: Session, room_id: int, check_in, check_out):
    
    return db.query(models.Reservation).filter(
        models.Reservation.room_id == room_id,
        models.Reservation.check_out > check_in,
        models.Reservation.check_in < check_out
    ).first()

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    guest = db.query(models.Guest).filter(models.Guest.id == reservation.guest_id).first()

    if not guest:
            raise HTTPException(status_code=404, detail='Guest not found')
    
    room = db.query(models.Room).filter(models.Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    
    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail='Check-out must be after check-in.')
    
    conflict = room_has_conflict(db, reservation.room_id, reservation.check_in, reservation.check_out)
    if conflict:
        raise HTTPException(status_code=400, detail='This room is already booked for the selected dates')
    
    db_reservation = models.Reservation(**reservation.model_dump())

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

def get_reservations(db: Session):
    return db.query(models.Reservation).all()

def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = get_reservation_by_id(db, reservation_id)

    if not reservation_id:
        return None
    
    db.delete(db_reservation)
    db.commit()

    return db_reservation