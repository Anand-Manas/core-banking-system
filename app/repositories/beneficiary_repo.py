from sqlalchemy.orm import Session
from app.models.beneficiary_model import Beneficiary


def get_beneficiaries_for_customer(db: Session, customer_id):
    return (
        db.query(Beneficiary)
        .filter(Beneficiary.customer_id == customer_id)
        .all()
    )
