"""
                APIs for posting, updating and deleting the bus details and its schedules
"""

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models import BusDetails, BusSchedules
from database import SessionLocal
from typing import Optional

router = APIRouter(
    prefix='/busadmin',
    tags=['busadmin']
)

# Function to get the db session and also to close the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Model for bus data with required fields
class BusData(BaseModel):
    bus_no: str = Field(..., title="Bus Number", max_length=30)
    from_to_location: str = Field(..., max_length=70, title="place1-place2")

# Model for bus schedule data with required fields
class BusScheduleData(BaseModel):
    bus_no: str = Field(..., title="Bus Number", max_length=30)
    from_to_location: str = Field(..., title="place1-place2", max_length=70)
    From: str = Field(..., title="From Place", max_length=50)
    departure_time: str = Field(..., max_length=20)
    To: str = Field(..., title="To Place", max_length=50)
    arriving_time: str = Field(..., max_length=20)
    stop_1: str = Field(..., max_length=50)
    stop_1_time: str = Field(..., max_length=20)
    stop_2: str = Field(..., max_length=50)
    stop_2_time: str = Field(..., max_length=20)
    stop_3: str = Field(..., max_length=50)
    stop_3_time: str = Field(..., max_length=20)
    stop_4: str = Field(..., max_length=50)
    stop_4_time: str = Field(..., max_length=20)
    stop_5: str = Field(..., max_length=50)
    stop_5_time: str = Field(..., max_length=20)
    stop_6: Optional[str] = Field(..., max_length=50)
    stop_6_time: Optional[str] = Field(..., max_length=20)
    stop_7: Optional[str] = Field(..., max_length=50)
    stop_7_time: Optional[str] = Field(..., max_length=20)
    
# Model for time schedule data with required fields
class TimeSchedule(BaseModel):
    bus_no: str = Field(..., title="Bus Number", max_length=30)
    from_to_location: str = Field(..., title="From-To place", max_length=70)
    From: str = Field(..., title="From Place", max_length=50)
    To: Optional[str] = Field(..., max_length=50)
    departure_time: str = Field(..., max_length=20)
    new_departure_time: Optional[str] = Field(..., max_length=20)
    arriving_time: str = Field(..., max_length=20)
    stop_1_time: str = Field(..., max_length=20)
    stop_2_time: str = Field(..., max_length=20)
    stop_3_time: str = Field(..., max_length=20)
    stop_4_time: str = Field(..., max_length=20)
    stop_5_time: str = Field(..., max_length=20)
    stop_6_time: Optional[str] = Field(..., max_length=20)
    stop_7_time: Optional[str] = Field(..., max_length=20)


# API to register the bus
@router.post('/register_bus', status_code=status.HTTP_201_CREATED)
async def register_bus(bus_data: BusData, db: Session = Depends(get_db)):

    # Check if the bus is already registered
    if db.query(BusDetails).filter((BusDetails.bus_no == bus_data.bus_no) & (BusDetails.from_to_location == bus_data.from_to_location)).first():
        raise HTTPException(status_code=400, detail="Bus already registered.")
    
    # Create a new BusDetails object with the provided bus data
    new_bus = BusDetails(
        bus_no = bus_data.bus_no.upper(),
        from_to_location = bus_data.from_to_location.lower()
    )

    # Add the new_bus object to the database session
    db.add(new_bus)
    db.commit()

    # Return a success message
    return {"message": "Bus registered successfully"}


# API to post the schedule for the registered bus
@router.post('/post_bus_schedule', status_code=status.HTTP_201_CREATED)
async def post_bus_schedule(bus_schedule: BusScheduleData, db: Session = Depends(get_db)):

    # Check if the bus is registered
    if not db.query(BusDetails).filter(BusDetails.bus_no == bus_schedule.bus_no.upper()).first():
        raise HTTPException(status_code=400, detail="Sorry! Register the bus to post its schedule.")
    
    # Get the bus details
    bus = db.query(BusDetails).filter((BusDetails.bus_no == bus_schedule.bus_no.upper()) & (BusDetails.from_to_location == bus_schedule.from_to_location.lower())).first()

    # Check if the bus runs for the given from-to-location
    if not bus:
        raise HTTPException(status_code=400, detail="Sorry! This bus doesn't run for the given from-to-location.")
    
    # Check if a schedule already exists for the exact departure time
    if db.query(BusSchedules).filter((BusSchedules.bus_id == bus.id) & (BusSchedules.From == bus_schedule.From.lower()) & (BusSchedules.departure_time == bus_schedule.departure_time.upper())).first():
        raise HTTPException(status_code=400, detail="Sorry! Schedule exists for the exact departure time.")
    
    # Create a new BusSchedules object with the provided schedule data
    schedule = BusSchedules(
        bus_id = bus.id,
        From = bus_schedule.From.lower(),
        departure_time = bus_schedule.departure_time.upper(),
        To = bus_schedule.To.lower(),
        arriving_time = bus_schedule.arriving_time.upper(),
        stop_1 = bus_schedule.stop_1.lower(),
        stop_1_time = bus_schedule.stop_1_time.upper(),
        stop_2 = bus_schedule.stop_2.lower(),
        stop_2_time = bus_schedule.stop_2_time.upper(),
        stop_3 = bus_schedule.stop_3.lower(),
        stop_3_time = bus_schedule.stop_3_time.upper(),
        stop_4 = bus_schedule.stop_4.lower(),
        stop_4_time = bus_schedule.stop_4_time.upper(),
        stop_5 = bus_schedule.stop_5.lower(),
        stop_5_time = bus_schedule.stop_5_time.upper(),
        stop_6 = bus_schedule.stop_6.lower(),
        stop_6_time = bus_schedule.stop_6_time.upper(),
        stop_7 = bus_schedule.stop_7.lower(),
        stop_7_time = bus_schedule.stop_7_time.upper()
    )

    # Add the schedule object to the database session
    db.add(schedule)
    db.commit()

    # Return a success message
    return {"message": "Bus schedule posted successfully."}


# API to post various time schedules for the existing one
@router.post('/post_another_schedule', status_code=status.HTTP_201_CREATED)
async def post_another_schedule(bus_schedule: TimeSchedule, db: Session = Depends(get_db)):
    # Check if the bus number is registered
    if not db.query(BusDetails).filter(BusDetails.bus_no == bus_schedule.bus_no.upper()).first():
        raise HTTPException(status_code=400, detail="Not a registered bus.")
    
    # Check if the bus runs for the given from-to-location
    bus = db.query(BusDetails).filter((BusDetails.bus_no == bus_schedule.bus_no.upper()) & (BusDetails.from_to_location == bus_schedule.from_to_location.lower())).first()
    if not bus:
        raise HTTPException(status_code=400, detail="Sorry! This bus doesn't run for the given from-to-location.")
    
    # Check if an schedule already exists for the given from and to place.
    bus_data = db.query(BusSchedules).filter((BusSchedules.bus_id == bus.id) & (BusSchedules.From == bus_schedule.From.lower()) & (BusSchedules.To == bus_schedule.To.lower())).first()
    if not bus_data:
        raise HTTPException(status_code=400, detail="Sorry! The bus doesn't run for the given from and to place.")
    
    # Check if an existing schedule already exists for the same given departure time
    if db.query(BusSchedules).filter((BusSchedules.bus_id == bus.id) & (BusSchedules.From == bus_schedule.From.lower()) & (BusSchedules.To == bus_schedule.To.lower()) & (BusSchedules.departure_time == bus_schedule.departure_time.upper())).first():
        raise HTTPException(status_code=400, detail="Sorry! Schedule exists  for the given departure time.")

    # Create a new BusSchedules object based on the provided details
    schedule = BusSchedules(
        bus_id = bus.id,
        From = bus_schedule.From.lower(),
        departure_time = bus_schedule.departure_time.upper(),
        To = bus_schedule.To.lower(),
        arriving_time = bus_schedule.arriving_time.upper(),
        stop_1 = bus_data.stop_1,
        stop_1_time = bus_schedule.stop_1_time.upper(),
        stop_2 = bus_data.stop_2,
        stop_2_time = bus_schedule.stop_2_time.upper(),
        stop_3 = bus_data.stop_3,
        stop_3_time = bus_schedule.stop_3_time.upper(),
        stop_4 = bus_data.stop_4,
        stop_4_time = bus_schedule.stop_4_time.upper(),
        stop_5 = bus_data.stop_5,
        stop_5_time = bus_schedule.stop_5_time.upper(),
        stop_6 = bus_data.stop_6,
        stop_6_time = bus_schedule.stop_6_time.upper(),
        stop_7 = bus_data.stop_7,
        stop_7_time = bus_schedule.stop_7_time.upper()
    )
    
    # Add and commit the new schedule to the database
    db.add(schedule)
    db.commit()

    # Return success message
    return {"message": "Bus schedule posted successfully."}

# API to update the existing bus' schedule completely
@router.put('/update_bus_schedule', status_code=status.HTTP_200_OK)
async def update_bus_schedule(new_bus_schedule: BusScheduleData, db: Session = Depends(get_db)):
    
    bus_data = db.query(BusDetails).filter(BusDetails.bus_no == new_bus_schedule.bus_no.upper() & (BusDetails.from_to_location == new_bus_schedule.from_to_location.lower())).first()
    if not bus_data:
        raise HTTPException(status_code=400, detail="Not a registered bus.")
    if not db.query(BusSchedules).filter((BusDetails.id == bus_data.id) & (BusSchedules.From == new_bus_schedule.From.lower())):
         raise HTTPException(status_code=400, detail="Sorry! Schedule not found for the given from place.")
    old_schedule = db.query(BusSchedules).filter((BusSchedules.bus_id == bus_data.id) & (BusSchedules.From == new_bus_schedule.From.lower()) & (BusSchedules.departure_time == new_bus_schedule.departure_time.upper())).first()
    if not old_schedule:
        raise HTTPException(status_code=400, detail="Sorry! old schedule not found.")

    old_schedule.From = new_bus_schedule.From.lower()
    old_schedule.departure_time = new_bus_schedule.departure_time.upper()
    old_schedule.To = new_bus_schedule.To.lower()
    old_schedule.arriving_time = new_bus_schedule.arriving_time.upper()
    old_schedule.stop_1 = new_bus_schedule.stop_1.lower()
    old_schedule.stop_1_time = new_bus_schedule.stop_1_time.upper()
    old_schedule.stop_2 = new_bus_schedule.stop_2.lower()
    old_schedule.stop_2_time = new_bus_schedule.stop_2_time.upper()
    old_schedule.stop_3 = new_bus_schedule.stop_3.lower()
    old_schedule.stop_3_time = new_bus_schedule.stop_3_time.upper()
    old_schedule.stop_4 = new_bus_schedule.stop_4.lower()
    old_schedule.stop_4_time = new_bus_schedule.stop_4_time.upper()
    old_schedule.stop_5 = new_bus_schedule.stop_5.lower()
    old_schedule.stop_5_time = new_bus_schedule.stop_5_time.upper()
    old_schedule.stop_6 = new_bus_schedule.stop_6.lower()
    old_schedule.stop_6_time = new_bus_schedule.stop_6_time.upper()
    old_schedule.stop_7 = new_bus_schedule.stop_7.lower()
    old_schedule.stop_7_time = new_bus_schedule.stop_7_time.upper()

    db.commit()

    return {"message": "Bus schedule updated successfully."}


# API to update the existing bus' time schedule 
@router.put('/update_time_schedule', status_code=status.HTTP_200_OK)
async def update_time_schedule(time_schedule: TimeSchedule, db: Session = Depends(get_db)):

    bus = db.query(BusDetails).filter((BusDetails.bus_no == time_schedule.bus_no.upper()) & (BusDetails.from_to_location == time_schedule.from_to_location.lower())).first()
    if not bus:
        raise HTTPException(status_code=400, detail="Sorry! Not a registered bus.")
    
    old_schedule = db.query(BusSchedules).filter((BusSchedules.bus_id == bus.id) & (BusSchedules.From == time_schedule.From.lower()) & (BusSchedules.departure_time == time_schedule.departure_time.upper())).first()
    if not old_schedule:
        raise HTTPException(status_code=400, detail="Sorry! No schedule exists for the exact departure time.")
    
    old_schedule.departure_time = time_schedule.new_departure_time.upper()
    old_schedule.arriving_time = time_schedule.arriving_time.upper()
    old_schedule.stop_1_time = time_schedule.stop_1_time.upper()
    old_schedule.stop_2_time = time_schedule.stop_2_time.upper()
    old_schedule.stop_3_time = time_schedule.stop_3_time.upper()
    old_schedule.stop_4_time = time_schedule.stop_4_time.upper()
    old_schedule.stop_5_time = time_schedule.stop_5_time.upper()
    old_schedule.stop_6_time = time_schedule.stop_6_time.upper()
    old_schedule.stop_7_time = time_schedule.stop_7_time.upper()

    db.commit()

    return {"message": "Bus schedule updated successfully."}


# API to delete the registered bus and its complete schedules
@router.delete('/delete_bus/{bus_no}/{from_to_location}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus(bus_no: str, from_to_location: str, db: Session = Depends(get_db)):
    bus = db.query(BusDetails).filter((BusDetails.bus_no == bus_no.upper()) & (BusDetails.from_to_location == from_to_location.lower())).first()
    if not bus:
        raise HTTPException(status_code=400, detail="Sorry! No bus found for the given data.")

    bus_schedules = db.query(BusSchedules).filter(BusSchedules.bus_id == bus.id).all()
    for schedule in bus_schedules:
        db.delete(schedule)

    db.delete(bus)
    db.commit()

    return {"message": "Bus and its schedules are deleted successfully."}


# API to delete the existing bus' schedule
@router.delete('/delete_bus_schedule/{bus_no}/{from_to_location}/{From}/{departure_time}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus_schedule(bus_no: str, from_to_location: str, From: str, departure_time: str, db: Session = Depends(get_db)):
    bus_data = db.query(BusDetails).filter((BusDetails.bus_no == bus_no.upper()) & (BusDetails.from_to_location == from_to_location.lower())).first()
    if not bus_data:
        raise HTTPException(status_code=400, detail="Sorry! No bus found")

    schedule = db.query(BusSchedules).filter((BusSchedules.bus_id == bus_data.id) & (BusSchedules.From == From.lower()) & (BusSchedules.departure_time == departure_time.upper())).first()
    if not schedule:
        raise HTTPException(status_code=400, detail="Sorry! Schedule not found.")

    db.delete(schedule)
    db.commit()

    return {"message": "Bus schedule is deleted successfully."}

