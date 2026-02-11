#OVERDRAFT LIMIT 

def test_overdraft_limit(client, admin_token, overdraft_account_id):
    payload = {
        "account_id": overdraft_account_id,
        "amount": 100000,
    }

    res = client.post(
        "/admin/debit",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert res.status_code == 400
    assert "Overdraft limit exceeded" in res.text
