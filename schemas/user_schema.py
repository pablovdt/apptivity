from typing import Optional, Any
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    city_cp: Optional[str] = None
    settings: Optional[Any] = None

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    city_cp: Optional[str]
    settings: Optional[Any]
    password: Optional[str]

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
