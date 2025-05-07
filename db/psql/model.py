import datetime

from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import Column, Integer, String, DateTime

from db.psql.connect import Base


def date_time_add_two_weeks():
    return datetime.datetime.now() + timedelta(weeks=2)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=1024), unique=True, index=True)
    password = Column(String(length=1024))
    created_at = Column(DateTime(), default=datetime.datetime.now)
    fire_end = Column(DateTime(), default=date_time_add_two_weeks)
