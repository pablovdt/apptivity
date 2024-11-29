from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

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
