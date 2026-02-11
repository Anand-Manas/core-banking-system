from sqlalchemy.orm import Session
from app.models.account_model import Account
from uuid import UUID
from fastapi import HTTPException

def get_account_for_update(db: Session, account_id: str):
    return (
        db.query(Account)
        .filter(Account.account_id == account_id)
        .with_for_update()
        .first()
    )




def lock_accounts_in_order(db, a_id, b_id):
    try:
        a_id = UUID(str(a_id))
        b_id = UUID(str(b_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account ID")

    first_id, second_id = sorted([a_id, b_id])

    first = (
        db.query(Account)
        .filter(Account.account_id == first_id)
        .with_for_update()
        .first()
    )

    second = (
        db.query(Account)
        .filter(Account.account_id == second_id)
        .with_for_update()
        .first()
    )

    if not first or not second:
        raise HTTPException(status_code=404, detail="Account not found")

    return first, second

