from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.models import customers, messages, reservations


@pytest.fixture()
def session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def make_customer(
    name: str = "Guest",
    email: str = "guest@example.com",
    notes: str | None = None,
) -> customers.Customer:
    return customers.Customer(
        name=name,
        email=email,
        phone_number="555-0000",
        notes=notes,
        created_at=datetime.now(timezone.utc),
    )


def test_reservation_caches_customer_notes(session: Session):
    customer = make_customer(notes="peanut allergy")
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=4,
        customer=customer,
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    assert reservation.status == "pending"
    assert reservation.customer_allergy_notes == "peanut allergy"
    assert reservation.reservation_notes is None


def test_reservation_status_validator(session: Session):
    customer = make_customer(name="Validator")
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=2,
        customer=customer,
    )

    with pytest.raises(ValueError):
        reservation.status = "bogus"


def test_message_requires_reservation(session: Session):
    customer = make_customer(name="Parser", email="parser@example.com")
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=3,
        customer=customer,
        status="needs_review",
    )
    session.add(reservation)
    session.commit()

    message = messages.Message(
        customer=customer,
        reservation=reservation,
        content="I have a peanut allergy",
        direction="inbound",
    )

    session.add(message)
    session.commit()

    stored_message = session.query(messages.Message).first()
    assert stored_message.reservation_id == reservation.id
    assert stored_message.direction == "inbound"


def test_message_without_reservation_fails(session: Session):
    customer = make_customer(name="NoReservation")
    session.add(customer)
    session.commit()

    message = messages.Message(
        customer=customer,
        reservation=None,
        content="Hello?",
        direction="inbound",
    )

    session.add(message)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
