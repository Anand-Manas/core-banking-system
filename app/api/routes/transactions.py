# Money transfer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import require_customer
from app.db.session import get_db
from app.schemas.transaction_schema import TransferRequest
from app.services.transaction_service import transfer_money
from app.models.customer_model import Customer
from app.models.account_model import Account

router = APIRouter()



@router.post(
    "/transfer",
    summary="Transfer Money",
    description="""
    Transfer money between two accounts owned by the customer.

    Features:
    - Atomic transaction
    - Row-level locking
    - Idempotency support
    """,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "transaction_id": "uuid",
                        "status": "SUCCESS"
                    }
                }
            }
        }
    }
)
def transfer(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    customer=Depends(require_customer),
):
    customer_obj = (
        db.query(Customer)
        .filter(Customer.user_id == customer.user_id)
        .first()
    )

    if not customer_obj:
        raise HTTPException(status_code=404, detail="Customer not found")

    destination_account = (
    db.query(Account)
    .filter(Account.account_number == payload.destination_account_number)
    .first()
    )

    if not destination_account:
        raise HTTPException(status_code=404, detail="Destination account not found")

    txn = transfer_money(
            db=db,
            customer_id=customer_obj.customer_id,
            source_account_id=payload.source_account_id,
            destination_account_id=destination_account.account_id,
            amount=payload.amount,
            idempotency_key=payload.idempotency_key,
        )

    db.commit()
    return {"transaction_id": str(txn.transaction_id),
            "status": txn.status,
        }
