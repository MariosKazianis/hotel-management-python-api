from pydantic import BaseModel
from datetime import date

class CustomerCreate(BaseModel):
    name:str
    email:str

class BookingCreate(BaseModel):
    customerId: int
    roomNumber: int
    checkIn: date
    checkOut: date
    pricePerNight: float