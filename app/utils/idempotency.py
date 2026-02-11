def normalize_idempotency_key(key: str) -> str:
    """
    Normalize idempotency key to avoid subtle mismatches.
    """
    return key.strip()
