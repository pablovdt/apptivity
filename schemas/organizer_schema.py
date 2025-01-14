from pydantic import BaseModel
from typing import Optional, List

from schemas.user_schema import UserOut


class OrganizerBase(BaseModel):
    name: str
    city_id: int
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    image_path: Optional[str] = None


class OrganizerCreate(OrganizerBase):
    password: str


class OrganizerUpdate(BaseModel):
    name: Optional[str] = None
    city_id: Optional[int] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    image_path: Optional[str] = None


class OrganizerOut(OrganizerBase):
    id: int
    city_longitude: Optional[float] = None
    city_latitude: Optional[float] = None
    users: List[UserOut] = None

    class Config:
        orm_mode = True


class OrganizerForUserOut(BaseModel):
    id: int
    name: str
    city_id: int
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
