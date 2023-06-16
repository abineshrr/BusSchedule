"""
                             Creating a BUS SCHEDULE MANAGEMENT SYSTEM using fastapi:

            "POST method for registering the bus and posting the bus' schedules"
            "GET method for fetching the respective bus' schedules using bus number, destination and from-to place"
            "PUT method for updating the existing bus' schedules"
            "DELETE method for deleting the respective bus' schedules and also we can delete complete bus and its all schedules"
"""

from fastapi import FastAPI
from database import engine, Base
from routers import busadmin, passengers

app = FastAPI(debug=True)
Base.metadata.create_all(bind=engine)

app.include_router(busadmin.router)
app.include_router(passengers.router)
