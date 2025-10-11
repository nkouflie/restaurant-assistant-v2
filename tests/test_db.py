from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from app.db import Base, SessionLocal, engine
from app.models import customers, reservations


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))


def test_create_customer():
    with SessionLocal() as session:
        customer = customers.Customer(
            name="Alice",
            email="alice@example.com",
            phone_number="123",
            notes="peanut allergy",
            created_at=datetime.now(timezone.utc),
        )
        session.add(customer)
        session.commit()

        result = (
            session.query(customers.Customer)
            .filter_by(email="alice@example.com")
            .first()
        )
        assert result is not None
        assert result.name == "Alice"
        assert result.notes == "peanut allergy"


def test_create_reservation_with_customer():
    with SessionLocal() as session:
        customer = customers.Customer(
            name="Bob",
            email="bob@example.com",
            phone_number="456",
            notes="tree nut allergy",
            created_at=datetime.now(timezone.utc),
        )
        reservation = reservations.Reservation(
            reservation_datetime=datetime.now(timezone.utc),
            party_size=2,
            customer=customer,
            reservation_notes="Birthday dinner",
        )
        session.add_all([customer, reservation])
        session.commit()
        session.refresh(reservation)

        assert reservation.customer.email == "bob@example.com"
        assert reservation.customer_allergy_notes == "tree nut allergy"
        assert reservation.reservation_notes == "Birthday dinner"
