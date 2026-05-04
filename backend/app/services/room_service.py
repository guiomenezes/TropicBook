from sqlalchemy.orm import Session
from app import models, schemas


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.model_dump())

    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room


def get_rooms(db: Session):
    return db.query(models.Room).all()


def get_room_by_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def update_room(db: Session, room_id: int, room: schemas.RoomCreate):
    db_room = get_room_by_id(db, room_id)

    if not db_room:
        return None

    db_room.name = room.name
    db_room.capacity = room.capacity
    db_room.price = room.price
    db_room.is_active = room.is_active

    db.commit()
    db.refresh(db_room)

    return db_room


def delete_room(db: Session, room_id: int):
    db_room = get_room_by_id(db, room_id)

    if not db_room:
        return None

    db.delete(db_room)
    db.commit()

    return db_room