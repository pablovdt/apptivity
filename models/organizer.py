from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Organizer(Base):
    __tablename__ = 'organizer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    description = Column(Text)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    image_path = Column(String(255))

    users = relationship('User', secondary='user_organizer', back_populates='organizers')
