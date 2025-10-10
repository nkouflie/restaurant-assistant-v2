from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .associations import (
    customer_dietary_restrictions,
    reservation_dietary_restrictions,
)


class DietaryRestriction(Base):

    __tablename__ = "dietary_restrictions"

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(250), nullable=True)

    # Relationships
    customers = relationship(
        "Customer",
        secondary=customer_dietary_restrictions,
        back_populates="dietary_restrictions",
    )
    reservations = relationship(
        "Reservation",
        secondary=reservation_dietary_restrictions,
        back_populates="dietary_restrictions",
    )
