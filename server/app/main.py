from fastapi import FastAPI, Depends, HTTPException
from . import models, schemas, service
from . import database
from typing import List
from sqlalchemy.orm import Session
# from . import utils
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database tables
models.Base.metadata.create_all(bind=database.engine)

# ------------------- API Endpoints -------------------

#  Fetch Available Slots
@app.get("/available-slots/{date}")
def get_available_slots(date: str, db: Session = Depends(get_db)):
    available_slots = service.get_available_slots(db, date)
    return available_slots

# book appointment
@app.post("/book-appointment/")
def book_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.date == appointment.date, 
        models.Appointment.time_slot == appointment.time_slot
    ).first()
    
    if existing_appointment:
        raise HTTPException(status_code=400, detail="This time slot is already booked.")
    
    service.create_appointment(db, appointment)
    return {"message": "Appointment booked successfully!"}

# View All Booked Appointments for a Date
@app.get("/appointments/{date}", response_model=List[schemas.Appointment])
def get_appointments(date: str, db: Session = Depends(get_db)):
    appointments = service.get_appointments(db, date)
    return appointments
