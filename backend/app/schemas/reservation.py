from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ResourceType(str, Enum):
    restaurant = "restaurant"
    show = "show"

class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ReservationBase(BaseModel):
    resource_type: ResourceType
    date: datetime
    nb_persons: Optional[int] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    resource_type: Optional[ResourceType] = None
    date: Optional[datetime] = None
    nb_persons: Optional[int] = None

class ReservationOut(ReservationBase):
    id: int
    user_id: int
    status: ReservationStatus

    class Config:
        from_attributes = True