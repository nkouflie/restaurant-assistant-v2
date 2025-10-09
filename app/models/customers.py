from ..db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .associations import customer_dietary_restrictions

class Customer(Base):

    __tablename__ = "customers"

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    reservations = relationship("Reservation", back_populates="customer")
    messages = relationship("Message", back_populates="customer")
    dietary_restrictions = relationship("DietaryRestriction", secondary=customer_dietary_restrictions, back_populates="customers")
