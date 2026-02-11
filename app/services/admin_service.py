from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password
from app.utils.password_validator import validate_password

from sqlalchemy.orm import Session
from app.models.customer_model import Customer
from app.models.account_model import Account
from app.schemas.admin_schemas import CreateCustomerRequest, CreateAccountRequest
from app.utils.account_number import generate_account_number



def create_admin(db, payload):
    # Ensure unique admin username
    existing_admin = (
        db.query(User)
        .filter(User.username == payload.username)
        .first()
    )

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with this username already exists",
        )

    # Validate password strength
    validate_password(payload.password)

    admin = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="ADMIN",
        status="ACTIVE",
        email=payload.email,
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Admin created successfully",
        "admin_id": admin.user_id,
    }

def create_customer(db: Session, payload: CreateCustomerRequest):
    # Check duplicate username
    existing_user = (
        db.query(User)
        .filter(User.username == payload.username)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="CUSTOMER",
        status="ACTIVE",
    )
    db.add(user)
    db.flush()  # IMPORTANT: get user_id without commit

    customer = Customer(
        user_id=user.user_id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        address=payload.address,
        customer_type=payload.customer_type,
    )
    db.add(customer)
    db.commit()

    return {
        "customer_id": customer.customer_id
    }


def create_account(db: Session, payload: CreateAccountRequest):
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == payload.customer_id)
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    account = Account(
        customer_id=payload.customer_id,
        account_number=generate_account_number(),
        account_type=payload.account_type,
        overdraft_limit=payload.overdraft_limit,
        balance=0,
        status="ACTIVE",
    )
    db.add(account)
    db.commit()

    return {
        "account_id": account.account_id,
        "account_number": account.account_number,
    }