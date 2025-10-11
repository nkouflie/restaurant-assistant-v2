from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import customers, messages, reservations


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def make_customer(session, phone: str = "+15550000001"):
    customer = customers.Customer(
        name="Guest",
        email="guest@example.com",
        phone_number=phone,
        notes="peanut allergy",
        created_at=datetime.now(timezone.utc),
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def make_reservation(session, customer):
    reservation = reservations.Reservation(
        reservation_datetime=datetime.now(timezone.utc),
        party_size=4,
        customer=customer,
        status="pending",
    )
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def test_receive_message_success():
    with TestingSessionLocal() as session:
        customer = make_customer(session)
        reservation = make_reservation(session, customer)

        response = client.post(
            "/messages/receive",
            data={
                "to_number": "+15550000000",
                "from_number": customer.phone_number,
                "body": "No allergies here!",
            },
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Message received"}

        stored = session.query(messages.Message).all()
        assert len(stored) == 1
        message = stored[0]
        assert message.content == "No allergies here!"
        session.refresh(reservation)
        assert reservation.status == "needs_review"


def test_receive_message_customer_not_found():
    response = client.post(
        "/messages/receive",
        data={
            "to_number": "+15550000000",
            "from_number": "+19999999999",
            "body": "Hello?",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_receive_message_no_active_reservation():
    with TestingSessionLocal() as session:
        customer = make_customer(session, phone="+15550000002")
        reservation = make_reservation(session, customer)
        reservation.status = "cancelled"
        session.commit()

    response = client.post(
        "/messages/receive",
        data={
            "to_number": "+15550000000",
            "from_number": "+15550000002",
            "body": "Checking on my booking",
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"] == "No active reservation found for customer"
    )
