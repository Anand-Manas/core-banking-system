from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.transaction_model import Transaction
from app.repositories.account_repo import get_account_for_update
from app.utils.cache import invalidate_cache
from app.services.audit_service import log_audit

from app.models.user import User
from app.models.customer_model import Customer
from app.models.account_model import Account
from app.core.security import hash_password
from app.core.logging import logger


def admin_debit(db: Session, admin_user_id, account_id: str, amount: Decimal):

    logger.info(f"Admin debit initiated | account_id={account_id} | amount={amount}")

    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debit amount must be greater than zero",
        )

    account = get_account_for_update(db, account_id)

    if not account or account.status != "ACTIVE":
        logger.warning(f"Admin credit FAILED | account not found | account_id={account_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is not active",
        )
    projected_balance = account.balance - amount

    if projected_balance < -account.overdraft_limit:
        logger.warning(f"Admin debit FAILED | overdraft exceeded | account={account.account_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Overdraft limit exceeded",
        )

    account.balance = projected_balance

    txn = Transaction(
        customer_id=account.customer_id,
        source_account_id=account.account_id,
        transaction_type="DEBIT",
        amount=amount,
        status="SUCCESS",
        idempotency_key=None,
    )

    db.add(txn)

    log_audit(
        db=db,
        user_id=admin_user_id,  # MUST be UUID
        action="ADMIN_DEBIT",
        entity="ACCOUNT",
        entity_id=account.account_id,
    )
    logger.info(f"Admin debit SUCCESS | account_id={account.account_id} | new_balance={account.balance}")
    invalidate_cache(
        f"account:{account.account_id}",
        f"accounts:customer:{account.customer_id}",
    )

    return txn


def admin_credit(db: Session, admin_user_id, account_id: str, amount: Decimal):
    logger.info(f"Admin credit initiated | account_id={account_id} | amount={amount}")
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit amount must be positive",
        )

    account = get_account_for_update(db, account_id)

    if not account or account.status != "ACTIVE":
        logger.warning(f"Admin debit FAILED | account not found | account_id={account_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account not active",
        )
    
    account.balance += amount

    txn = Transaction(
        customer_id=account.customer_id,
        destination_account_id=account.account_id,
        transaction_type="CREDIT",
        amount=amount,
        status="SUCCESS",
        idempotency_key=None,
    )

    db.add(txn)
    db.flush()

    log_audit(
        db=db,
        user_id=admin_user_id,  # MUST be UUID
        action="ADMIN_CREDIT",
        entity="ACCOUNT",
        entity_id=account.account_id,
    )
    
    logger.info(f"Admin credit SUCCESS | account_id={account.account_id} | new_balance={account.balance}")
    
    invalidate_cache(
        f"account:{account.account_id}",
        f"accounts:customer:{account.customer_id}",
    )

    return txn


def create_customer(db: Session, payload):
    existing_user = (
        db.query(User)
        .filter(User.username == payload.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with this username already exists",
        )

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role="CUSTOMER",
        status="ACTIVE",
    )
    db.add(user)
    db.flush()

    customer = Customer(
        user_id=user.user_id,
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        address=payload.address,
    )
    db.add(customer)
    db.commit()

    return {
        "message": "Customer created successfully",
        "customer_id": customer.customer_id,
    }


def create_account(db: Session, payload):
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == payload.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    account = Account(
        customer_id=payload.customer_id,
        account_type=payload.account_type,
        balance=0,
        overdraft_limit=payload.overdraft_limit,
        status="ACTIVE",
    )

    db.add(account)
    db.commit()

    return {
        "message": "Account created successfully",
        "account_id": account.account_id,
        "account_number": account.account_number,
    }
