from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, JSONB
from database import Base
from sqlalchemy.orm import relationship
from models.user_category import user_category


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    city_cp = Column(VARCHAR(10), ForeignKey('city.cp'))
    settings = Column(JSONB)
    categories = relationship('Category', secondary=user_category, back_populates='users')
    notification_distance = Column(Integer, nullable=True)
