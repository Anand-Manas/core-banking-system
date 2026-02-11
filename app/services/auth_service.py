from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repo import get_user_by_username
from app.core.security import verify_password, create_access_token
from app.services.audit_service import log_audit
from app.core.logging import logger


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user or not verify_password(password, user.password_hash):
        logger.warning(f"Login FAILED | username={username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if user.status != "ACTIVE":
        logger.warning(f"Login FAILED | username={username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is blocked"
        )

    token = create_access_token(
        data={
            "sub": str(user.user_id),
            "role": user.role
        }
    )
    log_audit(
        db=db,
        user_id=user.user_id,
        action="LOGIN_SUCCESS",
    )
    logger.info(f"Login success | user_id={user.user_id}")


    return {"access_token": token}
