from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Boolean, Double

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    user_name = Column(String)

    balance = Column(Double, default=0)

    wait_balance = Column(Double, default=0)

    total_balance = Column(Double, default=0)

    withdraw_balance = Column(Double, default=0)

    accept_license = Column(Boolean, default=False)

    is_enabled = Column(Boolean, default=False)

    registration_time = Column(DateTime, default=datetime.utcnow)

    refill_count = Column(Double, default=0)

    referrer_id = Column(Integer, default=None)

    has_payed_before = Column(Boolean, default=False)

    refill_from_referrer = Column(Integer, default=0)

    referrer_count = Column(Integer, default=0)

    time_to_action = Column(DateTime, default=None)

