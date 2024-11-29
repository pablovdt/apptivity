from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    users = relationship('User', secondary='user_category', back_populates='categories')
