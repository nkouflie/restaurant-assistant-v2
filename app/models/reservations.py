from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    event,
)
from sqlalchemy.orm import relationship, validates

from ..db import Base


class Reservation(Base):
    __tablename__ = "reservations"

    STATUSES = {"pending", "confirmed", "cancelled", "needs_review"}

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(
        Integer, ForeignKey("customers.id"), nullable=False, index=True
    )
    reservation_datetime = Column(
        DateTime(timezone=True), nullable=False, index=True
    )
    party_size = Column(Integer, nullable=False)
    status = Column(
        String(32),
        default="pending",
        server_default="pending",
        nullable=False,
    )
    customer_allergy_notes = Column(String(250), nullable=True)
    reservation_notes = Column(String(250), nullable=True)
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
    messages = relationship("Message", back_populates="reservation")

    @validates("status")
    def validate_status(self, _, value):
        """Validate the status of the reservation."""
        if value not in self.STATUSES:
            raise ValueError(f"Invalid status: {value}")
        return value

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'confirmed', 'cancelled', 'needs_review')",
            name="ck_reservation_status",
        ),
    )


@event.listens_for(Reservation, "before_insert")
def populate_customer_allergy_notes(mapper, connection, target):
    """Cache customer allergy notes onto the reservation if not provided."""
    if target.customer_allergy_notes:
        return
    customer = getattr(target, "customer", None)
    if customer and customer.notes:
        target.customer_allergy_notes = customer.notes
