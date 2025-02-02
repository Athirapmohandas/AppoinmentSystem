from pydantic import BaseModel
from typing import List

class AppointmentBase(BaseModel):
    name: str
    phone: str
    date: str  # Format: YYYY-MM-DD
    time_slot: str  # Format: HH:MM-HH:MM

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True

class AvailableSlots(BaseModel):
    available_slots: List[str]
