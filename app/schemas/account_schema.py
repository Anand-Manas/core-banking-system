from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID


class AccountCreate(BaseModel):
    customer_id: str
    account_type: str
    overdraft_limit: Decimal = 0

class CreateAccountRequest(BaseModel):
    customer_id: UUID
    account_type: str
    overdraft_limit: float