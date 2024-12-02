from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
from decimal import Decimal


class ActivityBase(BaseModel):
    name: Optional[str]
    place_id: Optional[int]
    date: Optional[datetime]
    price: Optional[Decimal]
    organizer_id: Optional[int]
    description: Optional[str]
    image_path:  Optional[str]
    category_id: Optional[int]
    cancelled: Optional[bool] = False
    number_of_assistances: Optional[int]
    number_of_shipments: Optional[int]
    number_of_discards: Optional[int]

class ActivityFilters(BaseModel):
    name: Optional[str] = None
    place_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    organizer_id: Optional[int] = None
    cancelled: Optional[bool] = None
    is_date_order_asc: bool = True
    order_by_assistance: Optional[bool] = None
    limit: Optional[int] = None


class ActivityCreate(ActivityBase):
    name: str
    place_id: int
    date: datetime
    price: float
    organizer_id: int
    description: str
    category_id: int


class ActivityUpdate(ActivityBase):
    pass


class ActivityOut(ActivityBase):
    id: int

    class Config:
        orm_mode = True

class ActivityForUserOut(BaseModel):
    id: int
    name: Optional[str]
    place_id: Optional[int]
    date: Optional[datetime]
    price: Optional[Decimal]
    organizer_id: Optional[int]
    organizer_name: Optional[str]
    description: Optional[str]
    image_path:  Optional[str]
    category_id: Optional[int]
    cancelled: Optional[bool] = False
    assistance: Union[bool, None]

    class Config:
        orm_mode = True
