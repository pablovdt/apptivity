from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Numeric
from sqlalchemy.dialects.postgresql import VARCHAR
from database import Base

class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    city_cp = Column(VARCHAR(10), ForeignKey('city.cp'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Numeric(10, 2))
    organizer_id = Column(Integer, ForeignKey('organizer.id'), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    cancelled = Column(Boolean, default=False)
    number_of_assistances = Column(Integer, default=0)
    number_of_shipments = Column(Integer, default=0)
    number_of_discards = Column(Integer, default=0)
