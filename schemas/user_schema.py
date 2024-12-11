from typing import Optional, Any, List, Union
from pydantic import BaseModel
from datetime import datetime

from schemas.activity_schema import ActivityForUserOut
from schemas.category_schema import CategoryOut
from schemas.level_schema import LevelOut


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
    level: Union[LevelOut, None] = None
    points: int = 0
    # level_id: int
    # level_name: str

    class Config:
        orm_mode = True

class UserActivityFilters(BaseModel):
    name: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    organizer_id: Optional[int] = None
    cancelled: Optional[bool] = None
    is_date_order_asc: bool = True
    all: Optional[bool] = None

class UserMoreActivitiesIn(BaseModel):
    user_id: Optional[int]
    categories_ids: List[int] = []

class ValidateQrLocation(BaseModel):
    activity_id: int
    organizer_id: int
    user_id: int
    latitude: float
    longitude: float