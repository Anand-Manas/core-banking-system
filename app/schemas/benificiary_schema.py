from pydantic import BaseModel


class BeneficiaryResponse(BaseModel):
    beneficiary_id: str
    beneficiary_account_number: str
    bank_name: str
    status: str
