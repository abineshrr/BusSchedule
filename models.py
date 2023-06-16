"""
            Database table models for storing bus details in bus_details table and storing bus' schedules in bus_schedules table
"""

from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class BusDetails(Base):
    __tablename__ = 'bus_details'

    id = Column(Integer, primary_key=True, index=True)
    bus_no = Column(String(30), index=True)
    from_to_location = Column(String(70), index=True)

    bus_schedules = relationship("BusSchedules", back_populates="bus_details")

class BusSchedules(Base):
    __tablename__ = 'bus_schedules'

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey('bus_details.id'))
    From = Column(String(50), index=True)
    departure_time = Column(String(30))
    To = Column(String(50), index=True)
    arriving_time = Column(String(30))
    stop_1 = Column(String(50))
    stop_1_time = Column(String(30))
    stop_2 = Column(String(50))
    stop_2_time = Column(String(30))
    stop_3 = Column(String(50))
    stop_3_time = Column(String(30))
    stop_4 = Column(String(50))
    stop_4_time = Column(String(30))
    stop_5 = Column(String(50))
    stop_5_time = Column(String(30))
    stop_6 = Column(String(50), nullable=True)
    stop_6_time = Column(String(30), nullable=True)
    stop_7 = Column(String(50), nullable=True)
    stop_7_time = Column(String(30), nullable=True)

    bus_details = relationship("BusDetails", back_populates="bus_schedules")
    
    