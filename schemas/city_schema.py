from pydantic import BaseModel
from typing import Optional

class CityBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CityOut(CityBase):
    cp: str

    class Config:
        orm_mode = True
