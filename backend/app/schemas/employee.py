from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssignmentItem(BaseModel):
    target_type: str

class EmployeeBase(BaseModel):
    name: str
    job: str
    assignment: Optional[List[AssignmentItem]] = []

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = None
    job: Optional[str] = None
    assignment: Optional[List[AssignmentItem]] = None


class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True