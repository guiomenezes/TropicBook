from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth.roles import require_role

router = APIRouter(
    prefix='/reservations',
    tags=['Reservations']
)


def room_has_conflict(db: Session, room_id: int, check_in, check_out, ignore_reservation_id: int = None):
    query = db.query(models.Reservation).filter(
        models.Reservation.room_id == room_id,
        models.Reservation.check_in < check_out,
        models.Reservation.check_out > check_in
    )

    if ignore_reservation_id:
        query = query.filter(models.Reservation.id != ignore_reservation_id)

    return query.first()


@router.post('/', response_model=schemas.ReservationResponse)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db), user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))):
    guest = db.query(models.Guest).filter(models.Guest.id == reservation.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail='Guest not found')

    room = db.query(models.Room).filter(models.Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')

    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail='Check-out must be after check-in')

    conflict = room_has_conflict(db, reservation.room_id, reservation.check_in, reservation.check_out)
    if conflict:
        raise HTTPException(status_code=400, detail='This room is already booked for the selected dates')

    db_reservation = models.Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation


@router.get('/', response_model=list[schemas.ReservationResponse])
def list_reservations(db: Session = Depends(get_db)):
    reservations = db.query(models.Reservation).all()
    return reservations


@router.get('/{reservation_id}', response_model=schemas.ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    if not db_reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')

    return db_reservation


@router.put('/{reservation_id}', response_model=schemas.ReservationResponse)
def update_reservation(reservation_id: int, reservation: schemas.ReservationCreate, db: Session = Depends(get_db), user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    if not db_reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')

    guest = db.query(models.Guest).filter(models.Guest.id == reservation.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail='Guest not found')

    room = db.query(models.Room).filter(models.Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')

    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail='Check-out must be after check-in')

    conflict = room_has_conflict(
        db,
        reservation.room_id,
        reservation.check_in,
        reservation.check_out,
        ignore_reservation_id=reservation_id
    )
    if conflict:
        raise HTTPException(status_code=400, detail='This room is already booked for the selected dates')

    db_reservation.guest_id = reservation.guest_id
    db_reservation.room_id = reservation.room_id
    db_reservation.check_in = reservation.check_in
    db_reservation.check_out = reservation.check_out

    db.commit()
    db.refresh(db_reservation)

    return db_reservation


@router.delete('/{reservation_id}')
def delete_reservation(reservation_id: int, db: Session = Depends(get_db), user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    if not db_reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')

    db.delete(db_reservation)
    db.commit()

    return {'message': 'Reservation deleted successfully.'}
