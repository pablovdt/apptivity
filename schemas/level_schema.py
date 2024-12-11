from pydantic import BaseModel



class LevelBase(BaseModel):
    name: str
    range_min: int
    range_max: int

class LevelOut(LevelBase):
    id: int