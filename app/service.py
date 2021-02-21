import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from app.db.database import SessionLocal
from app.db.database import engine3
from app.db.models import (
    Account,
    AccountModelIn,
    AccountModelOut,
    BookingModelIn,
    FlyBooking,
    HotelBooking,
    BookingModelOut,
)

db = SessionLocal()
logger = logging.getLogger(__name__)
SessionDB3 = sessionmaker(autocommit=False, autoflush=False, bind=engine3)
session_account = SessionDB3()


async def create_account(account_model: AccountModelIn):
    account = Account(**account_model.dict())
    session_account.add(account)
    session_account.commit()
    session_account.refresh(account)

    return AccountModelOut.from_orm(account)


async def create_booking(booking_model: BookingModelIn):
    booking = booking_model.dict()
    client_name = booking.get('client_name')
    prise = booking.get('price')
    fly_booking = FlyBooking(
        client_name=client_name,
        fly_number=booking.get('fly_number'),
        origin=booking.get('origin'),
        destination=booking.get('destination'),
        departure_date=booking.get('departure_date')
    )
    hotel_booking = HotelBooking(
        client_name=client_name,
        hotel_name=booking.get('hotel_name'),
        arrival_date=booking.get('arrival_to_hotel_date'),
        departure_date=booking.get('departure_from_hotel_date'),
    )
    try:
        db.add(hotel_booking)
        db.add(fly_booking)
        account = db.query(Account).filter(Account.client_name == client_name).first()
        if account:
            account.amount = account.amount - prise
            db.prepare()
            db.commit()
            db.refresh(fly_booking)
            db.refresh(hotel_booking)
            return BookingModelOut(
                hotel_booking_id=fly_booking.booking_id,
                fly_booking_id=hotel_booking.booking_id,
            )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=400, detail="Insufficient funds")
