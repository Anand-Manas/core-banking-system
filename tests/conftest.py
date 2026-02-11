import pytest
from fastapi.testclient import TestClient
from app.app import app
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.models.customer_model import Customer
import uuid

unique_id = str(uuid.uuid4())[:8]

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def admin_token(client):
    # Direct DB bootstrap (bypass protected API)
    db = SessionLocal()

    existing = db.query(User).filter(User.username == "test_admin").first()

    if not existing:
        admin = User(
            username="test_admin",
            password_hash=hash_password("admin123"),
            role="ADMIN",
            status="ACTIVE"
        )
        db.add(admin)
        db.commit()

    db.close()

    # Now login normally
    res = client.post(
        "/auth/login",
        data={
            "username": "test_admin",
            "password": "admin123"
        }
    )


    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture(scope="function")
def customer_token(client):

    db = SessionLocal()

    # 🔥 Generate new unique id per test
    unique_id = str(uuid.uuid4())[:8]

    user = User(
        username=f"test_user_{unique_id}",
        password_hash=hash_password("user123"),
        role="CUSTOMER",
        status="ACTIVE"
    )
    db.add(user)
    db.flush()

    customer = Customer(
        user_id=user.user_id,
        full_name="Test User",
        email=f"test_{unique_id}@example.com",
        phone=f"9{unique_id[:9]}",
        customer_type="INDIVIDUAL",
        address="Test City"
    )
    db.add(customer)
    db.commit()
    db.close()

    res = client.post(
        "/auth/login",
        data={
            "username": f"test_user_{unique_id}",
            "password": "user123"
        }
    )

    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture(scope="function")
def seeded_accounts(client, admin_token, customer_token):
    # Fetch customer profile
    profile = client.get(
        "/customer/profile",
        headers={"Authorization": f"Bearer {customer_token}"}
    ).json()

    customer_id = profile["customer_id"]

    # Create source account
    src = client.post(
        "/admin/accounts",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "customer_id": customer_id,
            "account_type": "SAVINGS",
            "overdraft_limit": 5000
        }
    ).json()

    # Create destination account
    dst = client.post(
        "/admin/accounts",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "customer_id": customer_id,
            "account_type": "SAVINGS",
            "overdraft_limit": 0
        }
    ).json()

    # Credit source account
    client.post(
        "/admin/credit",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "account_id": src["account_id"],
            "amount": 50000
        }
    )

    return src["account_id"], dst["account_number"]



@pytest.fixture
def overdraft_account_id(client, admin_token, customer_token):
    profile = client.get(
        "/customer/profile",
        headers={"Authorization": f"Bearer {customer_token}"}
    ).json()

    res = client.post(
        "/admin/accounts",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "customer_id": profile["customer_id"],
            "account_type": "SAVINGS",
            "overdraft_limit": 1000
        }
    )

    return res.json()["account_id"]
