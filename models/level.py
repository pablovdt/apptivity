from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    range_min = Column(Integer, nullable=False)
    range_max = Column(Integer, nullable=False)

    users = relationship('User', back_populates='level')