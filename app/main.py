from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import create_tables, get_db
from .models import customers, reservations


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
