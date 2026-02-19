import database
from fastapi import FastAPI
from models import Customer,Booking
from schemas import BookingCreate,CustomerCreate
from database import SessionDep
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

@app.post(
    "/customers",
    summary="Create a customer",
    response_description="The created customer",
)
def create_customer(customer: CustomerCreate , session: SessionDep) -> Customer:
    """
    Create a customer.
    - **id**: Optional integer. Generated automatically by the database.
    - **name**: Customer full name.
    - **email**: Customer email address.
    """
    newCustomer=Customer(
        name=customer.name,
        email=customer.email
    )
    session.add(newCustomer)
    session.commit()
    session.refresh(newCustomer)
    return newCustomer


@app.get("/customers")
def view_customers( session: SessionDep):
    statement= select(Customer)
    results=session.exec(statement)
    return results.all()

@app.post(
    "/bookings",
    summary="Create a booking" ,
    response_description="The created booking"
)
def create_booking(booking: BookingCreate, session: SessionDep)-> Booking:
    customer = session.get(Customer, booking.customerId)
    if not customer:
         raise HTTPException(status_code=404, detail="Customer not found")
    newBooking=Booking(
        customerId=booking.customerId,
        roomNumber=booking.roomNumber,
        checkIn=booking.checkIn,
        checkOut=booking.checkOut,
        pricePerNight=booking.pricePerNight
    )
    session.add(newBooking)
    session.commit()
    session.refresh(newBooking)
    return newBooking


@app.get("/bookings")
def view_bookings( session: SessionDep):
    statement= select(Booking)
    results=session.exec(statement)
    return results.all()