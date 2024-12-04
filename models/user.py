from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base
# necessary
from models.user_activity import user_activity

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'))
    settings = Column(JSONB)
    notification_distance = Column(Integer, nullable=True)

    categories = relationship('Category', secondary='user_category', back_populates='users')

    activities = relationship('Activity', secondary='user_activity', back_populates='users')

    organizers = relationship('Organizer', secondary='user_organizer', back_populates='users')