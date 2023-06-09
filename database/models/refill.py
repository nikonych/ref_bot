from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Double

from ..base import Base


class Refill(Base):
    __tablename__ = 'refills'

    user_id = Column(Integer)

    amount = Column(Double, default=0)

    refill_date = Column(DateTime, default=datetime.utcnow)

    refill_id = Column(String, primary_key=True)

    refill_type = Column(String, default="")
