from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import CheckConstraint
from sqlalchemy import Column, String, Integer, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)

Base = declarative_base()


class FlyBooking(Base):
    __tablename__ = "fly_booking"
    # __table_args__ = {'schema': 'db1'}

    booking_id = Column(Integer, nullable=True, index=False, primary_key=True, autoincrement=True)
    client_name = Column(String, nullable=True, unique=False, index=False)
    fly_number = Column(String, nullable=True, unique=False, index=False)
    origin = Column(String, nullable=True, unique=False, index=False)
    destination = Column(String, nullable=True, unique=False, index=False)
    departure_date = Column(Date, nullable=True, unique=False, index=False)

    # def __repr__(self):
    #     return str({
    #
    #     })


class HotelBooking(Base):
    __tablename__ = "hotel_booking"
    # __table_args__ = {'schema': 'db2'}

    booking_id = Column(Integer, nullable=True, index=False, primary_key=True, autoincrement=True)
    client_name = Column(String, nullable=True, unique=False, index=False)
    hotel_name = Column(String, nullable=True, unique=False, index=False)
    arrival_date = Column(Date, nullable=True, unique=False, index=False)
    departure_date = Column(Date, nullable=True, unique=False, index=False)


class Account(Base):
    __tablename__ = "account"
    # __table_args__ = {'schema': 'db3'}

    account_id = Column(Integer, nullable=True, index=False, primary_key=True, autoincrement=True)
    client_name = Column(String, nullable=True, unique=False, index=False)
    amount = Column(
        DECIMAL,
        CheckConstraint('amount>0'),
        nullable=False, unique=False, index=False
    )

    class Config:
        arbitrary_types_allowed = True


class AccountModelIn(BaseModel):
    client_name: str
    amount: Decimal

    class Config:
        orm_mode = True


class AccountModelOut(BaseModel):
    account_id: int
    client_name: str
    amount: Decimal

    class Config:
        orm_mode = True


class BookingModelIn(BaseModel):
    # hotel booking info
    client_name: str
    hotel_name: str
    arrival_to_hotel_date: date
    departure_from_hotel_date: date

    # fly booking info
    fly_number: str
    origin: str
    destination: str
    departure_date: date

    price: Decimal


class BookingModelOut(BaseModel):
    hotel_booking_id: Optional[int] = None
    fly_booking_id: Optional[int] = None
    message: Optional[str] = None
