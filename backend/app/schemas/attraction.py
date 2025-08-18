from pydantic import BaseModel
from enum import Enum
from typing import Optional

class AttractionStatus(str, Enum):
    open = "open"
    closed = "closed"
    maintenance = "maintenance"

class AttractionBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int
    status: AttractionStatus = AttractionStatus.open

class AttractionCreate(AttractionBase):
    pass

class AttractionOut(AttractionBase):
    id: int

    class Config:
        orm_mode = True