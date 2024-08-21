from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ActivityBase(BaseModel):
    name: Optional[str]
    place_id: Optional[int]
    date: Optional[datetime]
    price: Optional[Decimal]
    organizer_id: Optional[int]
    description: Optional[str]
    category_id: Optional[int]
    cancelled: Optional[bool] = False
    number_of_assistances: Optional[int]
    number_of_shipments: Optional[int]
    number_of_discards: Optional[int]


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
