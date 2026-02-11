from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

admin = User(
    username="admin",
    password_hash=hash_password("admin123"),
    role="ADMIN",
    status="ACTIVE"
)

db.add(admin)
db.commit()
db.close()
