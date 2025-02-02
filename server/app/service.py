from . import models
from sqlalchemy.orm import Session
from . import schemas
from . import utils

# create an appointment
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# get available slots for a specific date
def get_available_slots(db: Session, date: str):
    all_slots = utils.generate_slots()
    booked_slots = db.query(models.Appointment.time_slot).filter(models.Appointment.date == date).all()
    booked_slots_list = [str(slot[0]) for slot in booked_slots] 
    available_slots = [slot for slot in all_slots if slot not in booked_slots_list]

    return available_slots

# get appointments for a specific date
def get_appointments(db: Session, date: str):
    return db.query(models.Appointment).filter(models.Appointment.date == date).all()
