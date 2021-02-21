from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.models import FlyBooking, HotelBooking, Account

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pass@localhost"
DATABASE_URL_1 = "postgresql://postgres:pass@localhost/db1"
DATABASE_URL_2 = "postgresql://postgres:pass@localhost/db2"
DATABASE_URL_3 = "postgresql://postgres:pass@localhost/db3"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine1 = create_engine(DATABASE_URL_1)
engine2 = create_engine(DATABASE_URL_2)
engine3 = create_engine(DATABASE_URL_3)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, twophase=True)
SessionLocal.configure(binds={FlyBooking: engine1, HotelBooking: engine2, Account: engine3})
