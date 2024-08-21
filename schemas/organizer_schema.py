from typing import Optional
from pydantic import BaseModel


class OrganizerBase(BaseModel):
    name: str
    city_cp: str
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


class OrganizerCreate(OrganizerBase):
    pass


class OrganizerOut(OrganizerBase):
    id: int
