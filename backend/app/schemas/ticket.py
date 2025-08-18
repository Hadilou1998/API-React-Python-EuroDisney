from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    user_id: int
    attraction_id: int

class TicketCreate(TicketBase):
    pass

class TicketOut(TicketBase):
    id: int
    date: datetime
    qr_code: Optional[str] = None
    status: str

    class Config:
        orm_mode = True
