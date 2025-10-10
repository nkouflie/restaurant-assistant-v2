from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .associations import reservation_dietary_restrictions


class Reservation(Base):

    __tablename__ = "reservations"

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_datetime = Column(DateTime, nullable=False, index=True)
    party_size = Column(Integer, nullable=False)
    customer_id = Column(
        Integer, ForeignKey("customers.id"), nullable=False, index=True
    )
    occasion = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
    dietary_restrictions = relationship(
        "DietaryRestriction",
        secondary=reservation_dietary_restrictions,
        back_populates="reservations",
    )
