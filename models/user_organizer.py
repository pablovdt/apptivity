from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from database import Base
from datetime import datetime

user_organizer = Table(
    'user_organizer', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
    Column('organizer_id', Integer, ForeignKey('organizer.id', ondelete='CASCADE'), nullable=False),
    Column('inserted', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    Column('updated', DateTime(timezone=True), nullable=False, default=datetime.utcnow),
    PrimaryKeyConstraint('user_id', 'organizer_id')
)
