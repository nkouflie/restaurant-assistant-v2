from datetime import datetime

import pytest

from app.db import Base, SessionLocal, engine
from app.models import customers, dietary_restrictions, reservations


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test using CASCADE
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))


def test_create_customer():
    with SessionLocal() as session:
        customer = customers.Customer(
            name="Alice",
            email="alice@example.com",
            phone_number="123",
            created_at=datetime.utcnow(),
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
        result = (
            session.query(customers.Customer)
            .filter_by(email="alice@example.com")
            .first()
        )
        assert result is not None
        assert result.name == "Alice"


def test_create_dietary_restriction():
    with SessionLocal() as session:
        dr = dietary_restrictions.DietaryRestriction(name="Vegan")
        session.add(dr)
        session.commit()
        session.refresh(dr)
        result = (
            session.query(dietary_restrictions.DietaryRestriction)
            .filter_by(name="Vegan")
            .first()
        )
        assert result is not None
        assert result.name == "Vegan"


def test_create_reservation_with_customer_and_dietary_restriction():
    with SessionLocal() as session:
        customer = customers.Customer(
            name="Bob",
            email="bob@example.com",
            phone_number="456",
            created_at=datetime.utcnow(),
        )
        dr = dietary_restrictions.DietaryRestriction(name="Gluten-Free")
        reservation = reservations.Reservation(
            reservation_datetime=datetime.utcnow(),
            party_size=2,
            customer=customer,
            created_at=datetime.utcnow(),
        )
        # Set up relationships
        reservation.dietary_restrictions.append(dr)
        customer.dietary_restrictions.append(dr)
        session.add_all([customer, dr, reservation])
        session.commit()
        session.refresh(reservation)
        # Assertions
        res = (
            session.query(reservations.Reservation)
            .filter_by(customer_id=customer.id)
            .first()
        )
        assert res is not None
        assert res.customer.email == "bob@example.com"
        assert any(d.name == "Gluten-Free" for d in res.dietary_restrictions)
        assert any(d.name == "Gluten-Free" for d in customer.dietary_restrictions)
