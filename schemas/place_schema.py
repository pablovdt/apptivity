from typing import Optional
from pydantic import BaseModel

class PlaceBase(BaseModel):
    name: str
    city_cp: str

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    name: Optional[str]
    city_cp: Optional[str]

class PlaceOut(PlaceBase):
    id: int

    class Config:
        orm_mode = True
