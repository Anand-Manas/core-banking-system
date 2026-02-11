from sqlalchemy.orm import Session
from app.models.customer_model import Customer


def get_customer_by_id(db: Session, customer_id):
    return (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )
