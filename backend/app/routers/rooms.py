from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.auth.roles import require_role
from app.auth.deps import get_current_user
from app.services import room_service

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post('/', response_model=schemas.RoomResponse)
def create_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))
):
    return room_service.create_room(db, room)


@router.get('/', response_model=list[schemas.RoomResponse])
def list_rooms(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return room_service.get_rooms(db)


@router.get('/{room_id}', response_model=schemas.RoomResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    room = room_service.get_room_by_id(db, room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room


@router.put('/{room_id}', response_model=schemas.RoomResponse)
def update_room(
    room_id: int,
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN', 'RECEPCIONIST']))
):
    updated = room_service.update_room(db, room_id, room)

    if not updated:
        raise HTTPException(status_code=404, detail="Room not found")

    return updated


@router.delete('/{room_id}')
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role(['ADMIN']))
):
    result = room_service.delete_room(db, room_id)

    if not result:
        raise HTTPException(status_code=404, detail="Room not found")

    return {"message": "Deleted successfully"}