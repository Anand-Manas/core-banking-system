# Admin APIs
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.admin_schemas import AdminDebitCredit
from app.services.admin_transaction_service import admin_credit, admin_debit
from app.schemas.admin_schemas import CreateAdminRequest
from app.services import admin_service
#from app.schemas.customer_schema import CreateCustomerRequest
from app.schemas.account_schema import CreateAccountRequest
from app.schemas.admin_schemas import CreateCustomerRequest


router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(admin=Depends(require_admin)):
    return {"message": "Welcome Admin"}


@router.post(
    "/credit",
    summary="Credit Account",
    description="Credit money into a customer's account. Admin only.",
    responses={
        200: {
            "description": "Amount credited",
            "content": {
                "application/json": {
                    "example": {
                        "status": "credited",
                        "balance": 10000
                    }
                }
            }
        }
    }
)
def credit_account(
    payload: AdminDebitCredit,
    db: Session = Depends(get_db),
    admin = Depends(require_admin),   
):
    admin_credit(
        db=db,
        admin_user_id=admin.user_id, 
        account_id=payload.account_id,
        amount=payload.amount,
    )
    db.commit()
    return {"status": "credited"}


@router.post(
    "/debit",
    summary="Debit Account",
    description="Debit money from a customer's account with overdraft enforcement.",
    responses={
        200: {
            "description": "Amount debited",
            "content": {
                "application/json": {
                    "example": {
                        "status": "debited",
                        "balance": -3000
                    }
                }
            }
        },
        400: {"description": "Overdraft limit exceeded"}
    }
)
def debit_account(
    payload: AdminDebitCredit,
    db: Session = Depends(get_db),
    admin = Depends(require_admin),
):
    admin_debit(
        db=db,
        admin_user_id=admin.user_id,  
        account_id=payload.account_id,
        amount=payload.amount,
    )
    db.commit()
    return {f"status": "debited"}

@router.post(
    "/create-admin",
    summary="Create Admin User",
    description="""
    Create a new administrator account.

    ⚠️ Restricted access:
    - Only existing ADMIN users can call this endpoint
    - Used for controlled admin onboarding
    """,
    responses={
        200: {
            "description": "Admin created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "admin_id": "b3f9c2aa-8e7a-4b33-9f12-acde"
                    }
                }
            }
        },
        403: {"description": "Forbidden – Admin access required"}
    }
)
def create_admin(
    payload: CreateAdminRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return admin_service.create_admin(db, payload)

@router.post(
    "/customers",
    summary="Create Customer",
    description="Create a new customer. Admin only.",
    responses={
        200: {
            "description": "Customer created",
            "content": {
                "application/json": {
                    "example": {
                        "customer_id": "b6e2f4a4-3b5f-4a3e-9c21-acde"
                    }
                }
            }
        }
    }
)
def create_customer(
    payload: CreateCustomerRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return admin_service.create_customer(db, payload)

@router.post(
    "/accounts",
    summary="Create Account",
    description="Create a bank account for an existing customer. Admin only.",
    responses={
        200: {
            "description": "Account created",
            "content": {
                "application/json": {
                    "example": {
                        "account_id": "a1b2c3d4",
                        "account_number": "1234567890"
                    }
                }
            }
        }
    }
)
def create_account(
    payload: CreateAccountRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    return admin_service.create_account(db, payload)
