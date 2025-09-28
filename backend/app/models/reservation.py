import enum
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SAEnum, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class ResourceType(enum.Enum):
    restaurant = "restaurant"
    show = "show"

class ReservationStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_type = Column(SAEnum(ResourceType), nullable=False)
    date = Column(DateTime, default=datetime.now)
    nb_persons = Column(Integer, default=0)
    status = Column(SAEnum(ReservationStatus), default=ReservationStatus.pending)

    user = relationship("User", back_populates="reservations")