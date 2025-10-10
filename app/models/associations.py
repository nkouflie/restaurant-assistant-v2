from sqlalchemy import Column, ForeignKey, Integer, Table

from ..db import Base

customer_dietary_restrictions = Table(
    "customer_dietary_restrictions",
    Base.metadata,
    Column(
        "customer_id", Integer, ForeignKey("customers.id"), primary_key=True
    ),
    Column(
        "dietary_restriction_id",
        Integer,
        ForeignKey("dietary_restrictions.id"),
        primary_key=True,
    ),
)

reservation_dietary_restrictions = Table(
    "reservation_dietary_restrictions",
    Base.metadata,
    Column(
        "reservation_id",
        Integer,
        ForeignKey("reservations.id"),
        primary_key=True,
    ),
    Column(
        "dietary_restriction_id",
        Integer,
        ForeignKey("dietary_restrictions.id"),
        primary_key=True,
    ),
)
