from datetime import date

from sqlmodel import Field, SQLModel

class Customer(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    name:str
    email:str


class Booking(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    customerId:int = Field(foreign_key="customer.id")
    roomNumber:int
    checkIn:date
    checkOut:date
    pricePerNight:float

