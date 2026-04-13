from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, DateTime
from datetime import datetime
from app.database import Base

class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    document = Column(String)
    phone = Column(String)
    email = Column(String)

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    status = Column(String, nullable=False, default='AVAILABLE')

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey('guests.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='PENDING')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False, default='RECEPCIONIST')
    create_at = Column(DateTime, default=datetime.now)