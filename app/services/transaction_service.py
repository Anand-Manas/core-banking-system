from fastapi import HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.transaction_model import Transaction
from app.repositories.transaction_repo import get_by_idempotency
from app.repositories.account_repo import lock_accounts_in_order
from app.utils.cache import invalidate_cache
from app.services.audit_service import log_audit
from app.models.customer_model import Customer
from app.core.logging import logger


def transfer_money(
    db: Session,
    customer_id,
    source_account_id,
    destination_account_id,
    amount: Decimal,
    idempotency_key: str,
):
    logger.info(
        f"Transfer initiated | customer={customer_id} | "
        f"source={source_account_id} | destination={destination_account_id} | "
        f"amount={amount}"
    )

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    user_id = customer.user_id

    # 1️⃣ Idempotency short-circuit
    existing = get_by_idempotency(db, customer_id, idempotency_key)
    if existing:
        return existing

    # 2️⃣ Create PENDING transaction early
    txn = Transaction(
        customer_id=customer_id,
        source_account_id=source_account_id,
        destination_account_id=destination_account_id,
        transaction_type="TRANSFER",
        amount=amount,
        status="PENDING",
        idempotency_key=idempotency_key,
    )
    db.add(txn)
    db.flush()  # assigns transaction_id

    # 3️⃣ Lock accounts deterministically
    src, dst = lock_accounts_in_order(
        db, source_account_id, destination_account_id
    )

    # 4️⃣ Validate account status
    if src.status != "ACTIVE" or dst.status != "ACTIVE":
        txn.status = "FAILED"
        log_audit(
        db=db,
        user_id=user_id,
        action="TRANSFER_FAILED",
    )
        raise HTTPException(400, "Account not active")

    # 5️⃣ Overdraft validation
    projected = src.balance - amount
    if projected < -src.overdraft_limit:
        txn.status = "FAILED"
        log_audit(
            db=db,
            user_id=customer_id,
            action="TRANSFER_FAILED",
        )
        logger.warning(
        f"Transfer FAILED | overdraft exceeded | customer={customer_id}")

        raise HTTPException(400, "Overdraft limit exceeded")

    # 6️⃣ Apply balance changes
    src.balance = projected
    dst.balance += amount

    # 7️⃣ Mark SUCCESS
    txn.status = "SUCCESS"

    # 8️⃣ Audit SUCCESS
    log_audit(
        db=db,
        user_id=user_id,
        action="TRANSFER_SUCCESS",
        entity="TRANSACTION",
        entity_id=txn.transaction_id,
    )
    logger.info(f"Transfer SUCCESS | txn_id={txn.transaction_id}")

    # 9️⃣ Cache invalidation (AFTER success)
    invalidate_cache(
        f"account:{src.account_id}",
        f"account:{dst.account_id}",
        f"accounts:customer:{customer_id}",
    )

    return txn
