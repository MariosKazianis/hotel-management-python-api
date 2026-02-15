import database
from fastapi import FastAPI
from models import Customer
from database import SessionDep
from fastapi.middleware.cors import CORSMiddleware

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
    "/customers/",
    summary="Create a customer",
    response_description="The created customer",
)
async def create_customer(customer: Customer , session: SessionDep) -> Customer:
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


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        return {"error": "Customer not found"}
    return customer
