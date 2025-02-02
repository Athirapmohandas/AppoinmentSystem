from sqlalchemy import Column, Integer, String, UniqueConstraint
from .database import Base

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    date = Column(String)
    time_slot = Column(String)

    __table_args__ = (
        UniqueConstraint('date', 'time_slot', name='unique_appointment'),
    )
