# Customer APIs

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_customer
from app.db.session import get_db
from app.services.customer_service import get_customer_by_user
from app.services.account_service import (
    get_accounts_for_customer,
    get_account_for_customer
)

router = APIRouter()


@router.get(
    "/profile",
    summary="Get Customer Profile",
    description="Fetch the authenticated customer's profile.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "customer_id": "uuid",
                        "full_name": "John Doe",
                        "email": "john@test.com"
                    }
                }
            }
        }
    }
)
def get_profile(
    db: Session = Depends(get_db),
    user=Depends(require_customer),
):
    customer = get_customer_by_user(db, user)
    return customer


@router.get(
    "/accounts",
    summary="List Customer Accounts",
    description="List all accounts owned by the authenticated customer.",
)
def list_accounts(
    db: Session = Depends(get_db),
    user=Depends(require_customer),
):
    customer = get_customer_by_user(db, user)
    return get_accounts_for_customer(db, customer.customer_id)


@router.get(
    "/accounts/{account_id}",
    summary="Get Account",
    description="Fetch details of a specific account owned by the customer.",
)
def get_account(
    account_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_customer),
):
    customer = get_customer_by_user(db, user)
    return get_account_for_customer(db, customer.customer_id, account_id)

