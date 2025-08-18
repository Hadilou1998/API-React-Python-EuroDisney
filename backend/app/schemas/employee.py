from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class AssignmentItem(BaseModel):
    target_type: str

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    job: str
    assignment: Optional[List[AssignmentItem]] = []

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True