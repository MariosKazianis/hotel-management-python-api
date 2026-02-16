import database
from fastapi import FastAPI
from models import Customer
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
def create_customer(customer: Customer , session: SessionDep) -> Customer:
    """
    Create a customer.
    - **id**: Optional integer. Generated automatically by the database.
    - **name**: Customer full name.
    - **email**: Customer email address.
    """
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers")
def view_customers( session: SessionDep):
    statement= select(Customer)
    results=session.exec(statement)
    return results.all()
