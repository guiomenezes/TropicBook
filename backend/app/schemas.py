from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date, datetime

class GuestCreate(BaseModel):
    name: str
    last_name: str
    document: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class GuestResponse(BaseModel):
    id: int
    name: str
    last_name: str
    document: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    name: str
    capacity: int
    price: Decimal
    status: str = 'available'

class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    price: Decimal
    status: str

    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date

class ReservationResponse(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in: date
    check_out: date

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    reservation_id: int
    amount: float
    payment_method: str
    status: str ='PENDING'

class PaymentResponse(BaseModel):
    id: int
    reservation_id: int
    amount: float
    payment_date: datetime
    payment_method: str
    status: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str