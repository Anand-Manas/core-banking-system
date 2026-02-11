from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from typing import Optional
from enum import Enum

class CustomerType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"

class AdminDebitCredit(BaseModel):
    account_id: str
    amount: Decimal

class CreateAdminRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class CreateCustomerRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    full_name: str
    email: str
    phone: str
    address: str
    customer_type: CustomerType


class CreateAccountRequest(BaseModel):
    customer_id: str
    account_type: str
    overdraft_limit: float = 0