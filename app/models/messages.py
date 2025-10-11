from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base


class Message(Base):
    __tablename__ = "messages"

    # Column definitions
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(
        Integer, ForeignKey("customers.id"), nullable=False, index=True
    )
    reservation_id = Column(
        Integer, ForeignKey("reservations.id"), nullable=False, index=True
    )
    content = Column(Text, nullable=False)
    direction = Column(String(10), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    customer = relationship("Customer", back_populates="messages")
    reservation = relationship("Reservation", back_populates="messages")
