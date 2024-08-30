from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from database import Base

class Organizer(Base):
    __tablename__ = 'organizer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    city_cp = Column(VARCHAR(10), ForeignKey('city.cp'), nullable=False)
    description = Column(Text)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    image_path = Column(String(255))
