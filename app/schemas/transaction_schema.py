from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_number: str
    amount: Decimal
    idempotency_key: str
