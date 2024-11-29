from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import VARCHAR
from database import Base

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cp = Column(VARCHAR(10), nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_url = Column(VARCHAR(255))
