from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint
from database import Base

user_category = Table(
    'user_category', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
    Column('category_id', Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False),
    PrimaryKeyConstraint('user_id', 'category_id')
)
