from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ReservationBase(BaseModel):
    resource_type: str
    date: datetime
    nb_persons: Optional[int] = None

class ReservationCreate(ReservationBase):
    user_id: int

class ReservationUpdate(BaseModel):
    resource_type: Optional[str] = None
    date: Optional[datetime] = None
    nb_persons: Optional[int] = None
    status: Optional[ReservationStatus] = None

class ReservationOut(ReservationBase):
    id: int
    user_id: int
    status: ReservationStatus

    class Config:
        from_attributes = True
