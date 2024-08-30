from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from database import Base

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    location_url = Column(VARCHAR(255))
    city_cp = Column(VARCHAR(10), ForeignKey('city.cp'), nullable=False)
