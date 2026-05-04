from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.auth.roles import require_role
from app.auth.deps import get_current_user
from app.services import reservation_service

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.post('/', response_model=schemas.ReservationResponse)
def create_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))
):
    return reservation_service.create_reservation(db, reservation)


@router.get('/', response_model=list[schemas.ReservationResponse])
def list_reservations(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return reservation_service.get_reservations(db)


@router.get('/{reservation_id}', response_model=schemas.ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    reservation = reservation_service.get_reservation_by_id(db, reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return reservation


@router.delete('/{reservation_id}')
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN']))
):
    result = reservation_service.delete_reservation(db, reservation_id)

    if not result:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return {"message": "Deleted successfully"}
