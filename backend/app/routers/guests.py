from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix='/guests',
    tags=['Guests']
)

@router.post('/', response_model=schemas.GuestResponse)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    db_guest = models.Guest(**guest.model_dump())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)

    return db_guest

@router.get('/', response_model=list[schemas.GuestResponse])
def list_guests(db: Session = Depends(get_db)):
    guests = db.query(models.Guest).all()
    return guests

@router.get("/{guest_id}", response_model=schemas.GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()
    return guest

@router.put("/{guest_id}", response_model=schemas.GuestResponse)
def update_guest(guest_id: int, guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    db_guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()

    for key, value in guest.model_dump().items():
        setattr(db_guest, key, value)

    db.commit()
    db.refresh(db_guest)

    return db_guest

@router.delete("/{guest.id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    db_guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()

    if not db_guest:
        raise HTTPException(status_code=404, detail='Guest not found')

    db.delete(db_guest)
    db.commit()

    return {'message': 'Guest deleted.'}