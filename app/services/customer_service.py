from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.customer_model import Customer

CUSTOMER_TTL = 600


def get_customer_by_user(db: Session, user):
    customer = (
        db.query(Customer)
        .filter(Customer.user_id == user.user_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )

    return customer
