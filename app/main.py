from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import create_tables, get_db
from .models import customers, messages, reservations


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Restaurant Assistant API",
    description=(
        "A comprehensive API for managing restaurant customers, "
        "reservations, and messages"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://localhost:3001",  # Alternative React port
        "http://localhost:8080",  # Vue.js development server
        "http://localhost:4200",  # Angular development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def read_root():
    """Get API information and status."""
    return {"message": "Restaurant Assistant API", "status": "running"}


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


@app.get("/customers", tags=["Customers"])
def get_customers(db: Session = Depends(get_db)):
    """Get all customers."""
    customers_list = db.query(customers.Customer).all()
    return customers_list


@app.get("/reservations", tags=["Reservations"])
def get_reservations(db: Session = Depends(get_db)):
    """Get all reservations."""
    reservations_list = db.query(reservations.Reservation).all()
    return reservations_list


@app.post("/messages/receive", tags=["Messages"])
def receive_message(
    to_number: str = Form(...),
    from_number: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db),
):
    """Receive a message"""

    # Search for the customer by phone number
    customer = (
        db.query(customers.Customer)
        .filter_by(phone_number=from_number)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Find the most recent active reservation for the customer
    reservation = (
        db.query(reservations.Reservation)
        .filter_by(customer_id=customer.id)
        .filter(reservations.Reservation.status.in_(["pending", "confirmed"]))
        .order_by(reservations.Reservation.reservation_datetime.desc())
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=404, detail="No active reservation found for customer"
        )

    # Log the incoming message
    message = messages.Message(
        customer=customer,
        reservation=reservation,
        content=body,
        direction="inbound",
    )
    db.add(message)
    reservation.status = "needs_review"
    db.commit()

    return {"message": "Message received"}
