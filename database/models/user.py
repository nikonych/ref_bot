from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime, String

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    user_name = Column(String)

    balance = Column(Integer, default=0)

    token_count = Column(Integer, default=0)

    total_balance = Column(Integer, default=0)

    withdraw_balance = Column(Integer, default=0)

    wait_balance = Column(Integer, default=0)

    # registration_time = Column(DateTime, default=datetime.utcnow)
