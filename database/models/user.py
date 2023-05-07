from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Boolean

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    user_name = Column(String)

    balance = Column(Integer, default=0)

    wait_balance = Column(Integer, default=0)

    withdraw_balance = Column(Integer, default=0)

    is_enabled = Column(Boolean, default=False)

    registration_time = Column(DateTime, default=datetime.utcnow)

    refill_count = Column(Integer, default=0)

    refill_from_referrer = Column(Integer, default=0)

    referrer_count = Column(Integer, default=0)

    time_to_action = Column(DateTime, default=None)

