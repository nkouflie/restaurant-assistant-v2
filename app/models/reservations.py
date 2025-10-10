from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship, validates

from ..db import Base
from .associations import reservation_dietary_restrictions


class Reservation(Base):

    __tablename__ = "reservations"

    STATUSES = {"pending", "completed", "needs_review"}

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_datetime = Column(
        DateTime(timezone=True), nullable=False, index=True
    )
    party_size = Column(Integer, nullable=False)
    customer_id = Column(
        Integer, ForeignKey("customers.id"), nullable=False, index=True
    )
    occasion = Column(String(250), nullable=True)
    status = Column(
        String(32), default="pending", server_default="pending", nullable=False
    )
    allergy_summary = Column(String(250), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    customer = relationship("Customer", back_populates="reservations")
    dietary_restrictions = relationship(
        "DietaryRestriction",
        secondary=reservation_dietary_restrictions,
        back_populates="reservations",
    )
    messages = relationship("Message", back_populates="reservation")

    @validates("status")
    def validate_status(self, _, value):
        """Validate the status of the reservation."""
        if value not in self.STATUSES:
            raise ValueError(f"Invalid status: {value}")
        return value

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed', 'needs_review')",
            name="ck_reservation_status",
        ),
    )
