"""
                APIs for getting the bus' schedules - used by the passengers 
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models import BusDetails, BusSchedules
from database import SessionLocal

router = APIRouter(
    prefix='/passengers',
    tags=['passengers']
)

# Function to get the db session and also to close the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API to get the bus schedules by bus number
@router.get('/schedules_by_busNo/{bus_no}/{page}/{per_page}', status_code=status.HTTP_200_OK)
async def schedules_by_busNo(bus_no: str, page: int, per_page: int, db: Session = Depends(get_db)):
    # Check whether any bus matches for the given bus number
    if not db.query(BusDetails).filter(BusDetails.bus_no == bus_no.upper()).first():
        raise HTTPException(status_code=400, detail="No bus found for this bus number.")
    
    # Retrieve the bus schedule details for the given bus number using SQLAlchemy ORM
    schedules_query = db.query(BusSchedules).join(BusSchedules.bus_details).filter(BusDetails.bus_no == bus_no.upper())
    total_schedules = schedules_query.count()

    if not total_schedules:
        raise HTTPException(status_code=404, detail="No schedules found for this bus.")
    
    # Apply pagination
    schedules = schedules_query.offset((page - 1) * per_page).limit(per_page).all()

    # Convert the retrieved schedules to a list of dictionaries
    result = []
    for schedule in schedules:
        result.append({
            "bus_no": schedule.bus_details.bus_no,
            "From": schedule.From,
            "departure_time": schedule.departure_time,
            "To": schedule.To,
            "arriving_time": schedule.arriving_time,
            "stop_1": schedule.stop_1,
            "stop_1_time": schedule.stop_1_time,
            "stop_2": schedule.stop_2,
            "stop_2_time": schedule.stop_2_time,
            "stop_3": schedule.stop_3,
            "stop_3_time": schedule.stop_3_time,
            "stop_4": schedule.stop_4,
            "stop_4_time": schedule.stop_4_time,
            "stop_5": schedule.stop_5,
            "stop_5_time": schedule.stop_5_time,
            "stop_6": schedule.stop_6,
            "stop_6_time": schedule.stop_6_time,
            "stop_7": schedule.stop_7,
            "stop_7_time": schedule.stop_7_time
        })


    # Return the retrieved bus schedule details with pagination information
    return {
        "total_schedules": total_schedules,
        "schedules": result
    }


#API to get bus schedules for the given destination
@router.get('/schedules_by_To_place/{To_place}', status_code=status.HTTP_200_OK)
async def schedules_by_to(To_place: str, db: Session = Depends(get_db)):
    # Check whether any bus found for the given destination(To_place)
    bus = db.query(BusSchedules).filter(BusSchedules.To == To_place.lower()).first()
    if not bus:
        raise HTTPException(status_code=400, detail="No bus found for this destination.")

    # Retrieve the bus schedule details for the given destination using the ORM relationship
    schedules = db.query(BusSchedules).join(BusSchedules.bus_details).filter(BusSchedules.To == To_place.lower()).all()

    # Convert the retrieved schedules to a list of dictionaries
    result = []
    for schedule in schedules:
        result.append({
            "bus_no": schedule.bus_details.bus_no,
            "From": schedule.From,
            "departure_time": schedule.departure_time,
            "To": schedule.To,
            "arriving_time": schedule.arriving_time,
            "stop_1": schedule.stop_1,
            "stop_1_time": schedule.stop_1_time,
            "stop_2": schedule.stop_2,
            "stop_2_time": schedule.stop_2_time,
            "stop_3": schedule.stop_3,
            "stop_3_time": schedule.stop_3_time,
            "stop_4": schedule.stop_4,
            "stop_4_time": schedule.stop_4_time,
            "stop_5": schedule.stop_5,
            "stop_5_time": schedule.stop_5_time,
            "stop_6": schedule.stop_6,
            "stop_6_time": schedule.stop_6_time,
            "stop_7": schedule.stop_7,
            "stop_7_time": schedule.stop_7_time
        })

    # Return the retrieved bus schedule details
    return {
        "schedules_count": len(result),
        "schedules": result
    }


# API for getting the bus' shedules for the give from and to place
@router.get('/schedules_by_given_route/{from_place}/{To_place}', status_code=status.HTTP_200_OK)
async def schedules_by_from_and_to(from_place: str, To_place: str, db: Session = Depends(get_db)):

    # Query to fetch respective bus' schedules for the given from and to place by joining the bus_schedules and bus_details tables to show the respective bus number from the bus_details table in a logic 
    query = """
    SELECT bd.bus_no, bs."From", bs.departure_time, bs."To", bs.arriving_time, bs.stop_1, bs.stop_1_time,
            bs.stop_2, bs.stop_2_time, bs.stop_3, bs.stop_3_time, bs.stop_4, bs.stop_4_time,
            bs.stop_5, bs.stop_5_time, bs.stop_6, bs.stop_6_time, bs.stop_7, bs.stop_7_time
    FROM bus_schedules bs
    JOIN bus_details bd ON bs.bus_id = bd.id
    WHERE (
        bs."From" = :from_place OR
        bs.stop_1 = :from_place OR
        bs.stop_2 = :from_place OR
        bs.stop_3 = :from_place OR
        bs.stop_4 = :from_place OR
        bs.stop_5 = :from_place OR
        bs.stop_6 = :from_place OR
        bs.stop_7 = :from_place
    )
    AND (
        CASE
            WHEN bs."From" = :from_place THEN
                CASE
                    WHEN bs.stop_1 = :To_place THEN TRUE
                    WHEN bs.stop_2 = :To_place THEN TRUE
                    WHEN bs.stop_3 = :To_place THEN TRUE
                    WHEN bs.stop_4 = :To_place THEN TRUE
                    WHEN bs.stop_5 = :To_place THEN TRUE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_1 = :from_place THEN
                CASE
                    WHEN bs.stop_2 = :To_place THEN TRUE
                    WHEN bs.stop_3 = :To_place THEN TRUE
                    WHEN bs.stop_4 = :To_place THEN TRUE
                    WHEN bs.stop_5 = :To_place THEN TRUE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_2 = :from_place THEN
                CASE
                    WHEN bs.stop_3 = :To_place THEN TRUE
                    WHEN bs.stop_4 = :To_place THEN TRUE
                    WHEN bs.stop_5 = :To_place THEN TRUE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_3 = :from_place THEN
                CASE
                    WHEN bs.stop_4 = :To_place THEN TRUE
                    WHEN bs.stop_5 = :To_place THEN TRUE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_4 = :from_place THEN
                CASE
                    WHEN bs.stop_5 = :To_place THEN TRUE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_5 = :from_place THEN
                CASE
                    WHEN bs.stop_6 = :To_place THEN TRUE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            WHEN bs.stop_6 = :from_place THEN
                CASE
                    WHEN bs.stop_7 = :To_place THEN TRUE
                    ELSE FALSE
                END
            ELSE FALSE
        END
    )
    """

    result = db.execute(query, {
        "from_place": from_place.lower(),
        "To_place": To_place.lower()
    }).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="No bus found for this route.")
        
    schedules_count = len(result)
    schedules = [dict(row) for row in result]

    return {
        "schedules_count": schedules_count,
        "schedules": schedules
    }


# API to get every registered bus details
@router.get('/all_bus_details', status_code=status.HTTP_200_OK)
async def all_bus(page: int, per_page: int, db: Session = Depends(get_db)):
    # Retrieve the total number of buses
    total_buses = db.query(BusDetails).count()

    # Apply pagination
    buses = db.query(BusDetails).offset((page - 1) * per_page).limit(per_page).all()

    # Check if any bus is found
    if not buses:
        raise HTTPException(status_code=404, detail="No buses found.")

    # Return the retrieved bus details with pagination information
    return {
        "total_buses": total_buses,
        "buses": buses
    }


# API to get bus schedules of all registered buses
@router.get('/all_bus_schedules', status_code=status.HTTP_200_OK)
async def all_bus_schedules(page: int, per_page: int, db: Session = Depends(get_db)):
    # Retrieve the total number of schedules
    total_schedules = db.query(BusSchedules).count()

    # Apply pagination
    schedules = db.query(BusSchedules).offset((page - 1) * per_page).limit(per_page).all()

    # Check if any schedule is found
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found.")

    # Return the retrieved bus schedules with pagination information
    return {
        "total_schedules": total_schedules,
        "schedules": schedules
    }

