import enum
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SAEnum, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class ReservationStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_type = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.now)
    nb_persons = Column(Integer, default=1)
    status = Column(SAEnum(ReservationStatus, native_enum=False), default=ReservationStatus.pending)

    user = relationship("User", back_populates="reservations")