from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from database import Base
from datetime import datetime

user_activity = Table(
    'user_activity', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
    Column('activity_id', Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False),
    Column('possible_assistance', Boolean, default=None, nullable=True),
    Column('assistance', Boolean, default=None, nullable=True),
    Column('inserted', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    Column('updated', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    PrimaryKeyConstraint('user_id', 'activity_id')
)
