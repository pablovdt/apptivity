from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: Optional[str] = None

class CategoryCreate(CategoryBase):
    name: str

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
