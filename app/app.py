from fastapi import FastAPI
from app.api.routes import auth, admin, customer, transactions
from app.core.logging import logger

app = FastAPI(
    title="Core Banking System",
    description="""
    A production-grade Core Banking backend built using FastAPI.

    Key features:
    - Secure JWT authentication
    - Admin-controlled account lifecycle
    - Atomic money transfers
    - Controlled overdraft
    - Redis caching (read-only)
    - Audit logging for sensitive operations
    """,
    version="1.0.0",
)

logger.info("Application started")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(customer.router, prefix="/customer", tags=["Customer"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])