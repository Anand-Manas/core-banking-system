# test_db.py
from app.db.session import engine

try:
    conn = engine.connect()
    print("✅ Database connected successfully")
    conn.close()
except Exception as e:
    print("❌ DB connection failed:", e)
