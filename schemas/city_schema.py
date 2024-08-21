from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

class CityCreate(CityBase):
    cp: str

class CityOut(CityBase):
    cp: str

    class Config:
        orm_mode = True
