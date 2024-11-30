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
    name: Optional[str]
    email: Optional[str]
    city_id: Optional[int]
    settings: Optional[Any]
    password: Optional[str]
    notification_distance: Optional[int]
    category_ids: Optional[List[int]] = []

class UserOut(UserBase):
    id: int
    categories: List[CategoryOut]

    class Config:
        orm_mode = True
