import random


def generate_account_number() -> str:
    """
    Generates a 10-digit numeric account number.
    In real systems this would be sequence-based.
    """
    return str(random.randint(10**9, 10**10 - 1))
