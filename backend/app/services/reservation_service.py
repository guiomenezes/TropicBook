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
    
    nights = (reservation.check_out - reservation.check_in).days
    
    total_price = nights * float(room.price)

    db_reservation = models.Reservation(
        guest_id = reservation.guest_id,
        room_id = reservation.room_id,
        check_in = reservation.check_in,
        check_out = reservation.check_out,
        total_price = total_price,
        status = 'CONFIRMED'
    )

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    #Cria automaticamente o pagamento associado

    payment = models.Payment(
        reservation_id = db_reservation.id,
        amount = total_price,
        payment_method = 'CASH',
        status = 'PENDING'
    )

    db.add(payment)
    db.commit()

    return db_reservation

def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationUpdate):
    db_reservation = get_reservation_by_id(db, reservation_id)

    if not db_reservation:
        raise HTTPException(status_code=404, detail='Rservation not found')
    
    guest = db.query(models.Guest).filter(models.Guest.id == reservation.guest_id).first()

    if not guest:
        raise HTTPException(status_code=404, detail='Guest not found')

    room = db.query(models.Room).filter(models.Room.id == reservation.room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail='Room not found')

    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail='Check out must be after check in')
    
    conflict = db.query(models.Reservation).filter(
        models.Reservation.room_id == reservation.room_id,
        models.Reservation.id != reservation_id,
        models.Reservation.check_out > reservation.check_in,
        models.Reservation.check_in < reservation.check_out
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail='This room is already booked for the selected dates')
    
    nights = (reservation.check_out - reservation.check_in).days
    total_price = nights * float(room.price)

    db_reservation.guest_id = reservation.guest_id
    db_reservation.room_id = reservation.room_id
    db_reservation.check_in = reservation.check_in
    db_reservation.check_out = reservation.check_out
    db_reservation.total_price = total_price 
        
    payment = db.query(models.Payment).filter(models.Payment.reservation_id == reservation_id).first()

    if payment:
        payment.amount = total_price

    db.commit()
    db.refresh(db_reservation)

    return db_reservation

def get_reservations(db: Session):
    return db.query(models.Reservation).all()

def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = get_reservation_by_id(db, reservation_id)

    if not db_reservation:
        return None
    
    db.delete(db_reservation)
    db.commit()

    return db_reservation

def cancel_reservation(db:Session, reservation_id: int):
    reservation = get_reservation_by_id(db, reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')
    
    if reservation.status == 'CANCELLED':
        raise HTTPException(status_code=400, detail='Reservation is already cancelled')

    reservation.status = 'CANCELLED'

    payment = db.query(models.Payment).filter(models.Payment.reservation_id == reservation.id).first()

    if payment and payment.status == 'PENDING':
        payment.status = 'CANCELLED'
    
    db.commit()
    db.refresh(reservation)

    return reservation