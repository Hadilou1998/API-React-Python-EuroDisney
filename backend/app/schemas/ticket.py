from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    user_id: int
    attraction_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    user_id: Optional[int] = None
    attraction_id: Optional[int] = None

class TicketOut(TicketBase):
    id: int
    date: datetime
    qr_code: Optional[str] = None
    status: str

    class Config:
        orm_mode = True
