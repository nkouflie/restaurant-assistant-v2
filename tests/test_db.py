from app.db import engine, SessionLocal, Base
from app.models import customer, dietary_restrictions, reservations
from datetime import datetime

Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    # Clean up any existing test data first
    session.query(customer.Customer).filter_by(email="john.doe@example.com").delete()
    session.query(dietary_restrictions.DietaryRestriction).filter_by(name="Vegan").delete()
    session.commit()

    new_customer = customer.Customer(name="John Doe", email="john.doe@example.com", phone_number="555-1234")
    new_dietary_restriction = dietary_restrictions.DietaryRestriction(name="Vegan")
    new_reservation = reservations.Reservation(reservation_datetime=datetime.utcnow(), party_size=4, customer=new_customer, created_at=datetime.utcnow())
    
    new_reservation.dietary_restrictions.append(new_dietary_restriction)
    new_customer.dietary_restrictions.append(new_dietary_restriction)

    session.add_all([new_customer, new_dietary_restriction, new_reservation])
    session.commit()

    print("Test data inserted successfully.")
    customers = session.query(customer.Customer).all()
    for cust in customers:
        print(f"Customer: {cust.name}, Dietary Restrictions: {[dr.name for dr in cust.dietary_restrictions]}")
    reservations_list = session.query(reservations.Reservation).all()
    for res in reservations_list:
        print(f"Reservation ID: {res.id}, Customer: {res.customer.name}, Dietary Restrictions: {[dr.name for dr in res.dietary_restrictions]}")
    dietary_restrictions_list = session.query(dietary_restrictions.DietaryRestriction).all()
    for dr in dietary_restrictions_list:
        print(f"Dietary Restriction: {dr.name}, Customers: {[cust.name for cust in dr.customers]}, Reservations: {[res.id for res in dr.reservations]}")
    
    session.close()