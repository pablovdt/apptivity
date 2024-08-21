from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

# Tabla de asociación entre User y Category
user_category = Table(
    'user_category',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)
