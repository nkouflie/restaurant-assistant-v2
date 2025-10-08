from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db, create_tables
from .models import customer, reservations, dietary_restrictions, message
import logging

app = FastAPI(title="Restaurant Assistant API", version="1.0.0")

# Create tables on startup
@app.on_event("startup")
async def startup():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Restaurant Assistant API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(customer.Customer).all()
    return customers

@app.get("/reservations")
def get_reservations(db: Session = Depends(get_db)):
    reservations_list = db.query(reservations.Reservation).all()
    return reservations_list
