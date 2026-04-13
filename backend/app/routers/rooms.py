from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix='/rooms',
    tags=['Rooms']
)

@router.post('/', response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = models.Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room

@router.get('/', response_model=list[schemas.RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    
    return rooms

@router.get('/{room_id}', response_model=schemas.RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail='Room not found')
    
    return db_room

@router.put('/{room_id}', response_model=schemas.RoomResponse)
def update_room(room_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail='Room not found')
    
    db_room.name = room.name
    db_room.capacity = room.capacity
    db_room.price = room.price
    db_room.status = room.status

    db.commit()
    db.refresh(db_room)

    return db_room

@router.delete('/{room_id}')
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail='Room not found')
        
    db.delete(db_room)
    db.commit()

    return {"message": "Room deleted successfully."}