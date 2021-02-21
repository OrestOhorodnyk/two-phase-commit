import logging

from fastapi import APIRouter

from app.db.models import (
    AccountModelIn,
    AccountModelOut,
    BookingModelIn,
    BookingModelOut,
)
from app.service import (
    create_account,
    create_booking,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    return {"status": "ok"}


@router.post("/account", status_code=201, response_model=AccountModelOut)
async def create_user_account(account: AccountModelIn):
    return await create_account(account)


@router.post("/booking", status_code=201, response_model=BookingModelOut)
async def create_user_booking(booking_model: BookingModelIn):
    logger.info(f'Booking IN: {booking_model}')
    return await create_booking(booking_model)
