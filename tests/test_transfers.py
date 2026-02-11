#ATOMIC TRANSFER : This validates atomicity at the API boundary
import logging
logger = logging.getLogger("pytest")

def test_atomic_transfer(client, customer_token, seeded_accounts):
    logger.info("Running atomic transfer test")
    src_id, dst_number = seeded_accounts
    payload = {
        "source_account_id": src_id,
        "destination_account_number": dst_number,
        "amount": 100.0,
        "idempotency_key": "atomic-001",
    }
    
    res = client.post(
        "/transactions/transfer",
        json=payload,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    
    assert res.status_code == 200

    data = res.json()

    assert "transaction_id" in data
    assert data["status"] == "SUCCESS"


#IDEMPOTENCY

def test_idempotency(client, customer_token, seeded_accounts):
    src_id, dst_number = seeded_accounts

    before = client.get(
        f"/customer/accounts/{src_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    ).json()["balance"]

    payload = {
        "source_account_id": src_id,
        "destination_account_number": dst_number,
        "amount": 500,
        "idempotency_key": "idem-001",
    }

    res1 = client.post(
        "/transactions/transfer",
        json=payload,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    print("RES1:", res1.status_code, res1.json())

    res2 = client.post(
        "/transactions/transfer",
        json=payload,
        headers={"Authorization": f"Bearer {customer_token}"}
    )
    print("RES2:", res2.status_code, res2.json())

    assert res1.status_code == 200
    assert res2.status_code == 200

    after = client.get(
        f"/customer/accounts/{src_id}",
        headers={"Authorization": f"Bearer {customer_token}"}
    ).json()["balance"]

    # Deducted only once
    assert before - after == 500

