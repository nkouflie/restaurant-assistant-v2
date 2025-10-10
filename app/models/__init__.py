# Import order matters for relationship resolution
from .associations import (
    customer_dietary_restrictions,
    reservation_dietary_restrictions,
)
from .customers import Customer
from .dietary_restrictions import DietaryRestriction
from .messages import Message
from .reservations import Reservation

__all__ = [
    "Customer",
    "DietaryRestriction",
    "Message",
    "Reservation",
    "customer_dietary_restrictions",
    "reservation_dietary_restrictions",
]
