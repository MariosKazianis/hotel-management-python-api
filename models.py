import datetime

from sqlmodel import Field, SQLModel

class Customer(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    name:str
    email:str


class Stay(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    customerId:int = Field(foreign_key="customer.id")
    roomNumber:int
    checkIn:datetime.date
    checkOut:datetime.date
    pricePerNight:float

