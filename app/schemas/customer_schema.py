from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: EmailStr
    phone: str
    customer_type: str
    address: str

class CreateCustomerRequest(BaseModel):
    username: str
    password: str
    full_name: str
    email: EmailStr
    phone: str
    address: str

