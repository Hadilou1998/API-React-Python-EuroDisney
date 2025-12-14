from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class LoginJSON(BaseModel):
    email: str
    password: str