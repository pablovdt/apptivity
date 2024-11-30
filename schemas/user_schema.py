from typing import Optional, Any, List
from pydantic import BaseModel

from models import Category
from schemas.category_schema import CategoryOut


class UserBase(BaseModel):
    name: str
    email: str
    city_id: Optional[int] = None
    settings: Optional[Any] = None
    notification_distance: Optional[int]

class UserCreate(UserBase):
    password: str
    category_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str = None
    email: str = None
    city_id: int = None
    settings: Any = None
    password: str = None
    notification_distance: int = None
    categories: List[int] = []

class UserOut(UserBase):
    id: int
    categories: List[CategoryOut]

    class Config:
        orm_mode = True
