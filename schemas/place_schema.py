from pydantic import BaseModel

class PlaceBase(BaseModel):
    name: str
    city_cp: str

    class Config:
        orm_mode = True

class PlaceCreate(PlaceBase):
    pass

class PlaceOut(PlaceBase):
    id: int
