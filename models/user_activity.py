from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint
from database import Base

user_activity = Table(
    'user_activity', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
    Column('activity_id', Integer, ForeignKey('activity.id', ondelete='CASCADE'), nullable=False),
    PrimaryKeyConstraint('user_id', 'activity_id')
)
