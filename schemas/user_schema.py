from pydantic import BaseModel, EmailStr
from typing import Any


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    city_cp: str
    settings: Any

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    city_cp: str
    settings: Any

    class Config:
        orm_mode = True
