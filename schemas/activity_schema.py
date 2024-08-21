from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ActivityBase(BaseModel):
    name: str
    city_cp: str
    date: datetime
    price: Optional[float] = None
    organizer_id: int
    description: Optional[str] = None
    category_id: int
    cancelled: Optional[bool] = False
    number_of_assistances: Optional[int] = 0
    number_of_shipments: Optional[int] = 0
    number_of_discards: Optional[int] = 0

    class Config:
        orm_mode = True

class ActivityCreate(ActivityBase):
    pass

class ActivityOut(ActivityBase):
    id: int
