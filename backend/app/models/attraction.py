from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base
import enum

class AttractionStatus(str, enum.Enum):
    open = "open"
    closed = "closed"
    maintenance = "maintenance"

class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    capacity = Column(Integer, nullable=False)
    status = Column(Enum(AttractionStatus), default=AttractionStatus.open)