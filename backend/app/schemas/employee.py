from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    job: str
    assignment: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = None
    job: Optional[str] = None
    assignment: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True