from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.models import customers, dietary_restrictions, messages, reservations


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
    name: str = "Guest", email: str = "guest@example.com"
) -> customers.Customer:
    return customers.Customer(
        name=name,
        email=email,
        phone_number="555-0000",
        created_at=datetime.now(timezone.utc),
    )


def test_reservation_defaults(session: Session):
    customer = make_customer()
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=4,
        customer=customer,
        created_at=datetime.now(timezone.utc),
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    assert reservation.status == "pending"
    assert reservation.allergy_summary is None


def test_reservation_status_validator(session: Session):
    customer = make_customer(name="Validator")
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=2,
        customer=customer,
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(ValueError):
        reservation.status = "bogus"


def test_message_parser_fields(session: Session):
    customer = make_customer(name="Parser", email="parser@example.com")
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=3,
        customer=customer,
        created_at=datetime.now(timezone.utc),
        allergy_summary="peanut allergy",
        status="needs_review",
    )
    message = messages.Message(
        customer=customer,
        reservation=reservation,
        content="I have a peanut allergy",
        direction="inbound",
        intent="allergy_update",
        confidence=0.82,
    )
    tag = dietary_restrictions.DietaryRestriction(name="peanut")

    reservation.dietary_restrictions.append(tag)
    session.add_all([reservation, message, tag])
    session.commit()
    session.refresh(message)

    stored_message = session.query(messages.Message).first()
    assert stored_message.intent == "allergy_update"
    assert stored_message.confidence == pytest.approx(0.82)
    assert stored_message.reservation.status == "needs_review"
    assert any(
        dr.name == "peanut"
        for dr in stored_message.reservation.dietary_restrictions
    )
