from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Boolean, Double

from ..base import Base


class Withdraw(Base):
    __tablename__ = 'withdraws'

    user_id = Column(Integer)

    amount = Column(Double, default=0)

    withdraw_date = Column(DateTime, default=datetime.utcnow)

    withdraw_id = Column(String, primary_key=True)

    withdraw_type = Column(String, default="")

    withdraw_number = Column(String, default="")

    withdraw_status = Column(String, default="WAITING")
