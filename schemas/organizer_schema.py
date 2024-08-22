from pydantic import BaseModel
from typing import Optional


class OrganizerBase(BaseModel):
    name: str
    city_cp: str
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str


class OrganizerCreate(OrganizerBase):
    password: str


class OrganizerUpdate(BaseModel):
    name: Optional[str] = None
    city_cp: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str  #


class OrganizerOut(OrganizerBase):
    id: int

    class Config:
        orm_mode = True
