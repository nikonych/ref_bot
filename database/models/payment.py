from datetime import datetime

from sqlalchemy import Column, Integer, String

from ..base import Base


class Payment(Base):
    __tablename__ = 'payments'

    name = Column(String)

    token = Column(String, nullable=True)

    balance = Column(Integer, default=0)

    client_id = Column(String, nullable=True)

    secret_phrase = Column(String, nullable=True)

