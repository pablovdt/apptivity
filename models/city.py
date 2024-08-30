from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import VARCHAR
from database import Base

class City(Base):
    __tablename__ = 'city'

    cp = Column(VARCHAR(10), primary_key=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_url = Column(VARCHAR(255))
