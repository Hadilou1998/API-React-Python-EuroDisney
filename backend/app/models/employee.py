from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    job = Column(String(100), nullable=False)
    assignment = Column(String(255), nullable=True)