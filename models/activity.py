from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base
# necessary
from models.user_activity import user_activity

class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Numeric(10, 2))
    organizer_id = Column(Integer, ForeignKey('organizer.id'), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    cancelled = Column(Boolean, default=False)
    number_of_assistances = Column(Integer, default=0)
    number_of_shipments = Column(Integer, default=0)
    number_of_discards = Column(Integer, default=0)
    image_path = Column(String(255))

    users = relationship('User', secondary='user_activity', back_populates='activities')
