from sqlalchemy.orm import Session
from app.models.transaction_model import Transaction

def get_by_idempotency(db: Session, customer_id, key):
    return (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer_id,
            Transaction.idempotency_key == key
        )
        .first()
    )
