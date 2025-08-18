from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    attraction_id = Column(Integer, ForeignKey("attractions.id"))
    date = Column(DateTime, default=datetime.now())
    qr_code = Column(String(255), nullable=False)
    status = Column(String(20), default="active") # active, used, expired, cancelled

    user = relationship("User", backref="tickets")
    attraction = relationship("Attraction", backref="tickets")