from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, JSONB
from database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    city_cp = Column(VARCHAR(10), ForeignKey('city.cp'))
    settings = Column(JSONB)
