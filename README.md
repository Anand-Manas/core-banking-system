# 🏦 Core Banking System Backend

A production-grade Core Banking backend built using **FastAPI**, focused on transactional correctness, security, and system design principles rather than CRUD completeness.

---

## 🚀 Overview

This project simulates a simplified core banking system with:

- Secure JWT-based authentication (Admin & Customer roles)
- Controlled overdraft enforcement
- Atomic money transfers with row-level locking
- Per-customer idempotency protection
- Redis cache-aside strategy for read-heavy endpoints
- Audit logging for sensitive operations
- High-signal automated tests

The system is designed with **correctness, isolation, and traceability** as primary goals.

---

## 🏗 Architecture Overview

The application follows a layered architecture:

Client
↓
Routes (API Layer)
↓
Services (Business Logic)
↓
Repositories (Data Access)
↓
PostgreSQL (Source of Truth)


Additional components:

- 🔐 JWT Authentication (Stateless)
- ⚡ Redis (Read-only cache)
- 📜 Audit Logging (Best-effort, non-blocking)
- 🧪 Pytest Integration Tests

---

## 🧩 Key Design Decisions

### 1️⃣ Database as Source of Truth
All financial decisions rely strictly on PostgreSQL.  
Redis is used only for read optimization.

---

### 2️⃣ Atomic Money Transfers

Transfers are implemented using:

- Row-level locking (`SELECT FOR UPDATE`)
- Deterministic lock ordering (to prevent deadlocks)
- Single database transaction commit

Guarantee:
> Money is neither lost nor duplicated.

---

### 3️⃣ Controlled Overdraft Logic

Each account has an `overdraft_limit`.

Debit logic ensures:

balance - amount >= -overdraft_limit


This enforces strict financial boundaries.

---

### 4️⃣ Per-Customer Idempotency

Each transfer requires an `idempotency_key`.

If the same request is retried:
- The original transaction result is returned
- No duplicate execution occurs

Prevents double-spending due to retries or network failures.

---

### 5️⃣ Redis Cache-Aside Strategy

Cached Endpoints:
- Customer profile
- Account list
- Account details

Write operations:
- Explicitly invalidate relevant cache keys
- Cache never acts as authority

---

### 6️⃣ Audit Logging

Sensitive actions are logged:

- Login success
- Admin credit/debit
- Transfer success/failure

Design principle:
> Audit logging must never block core transactions.

---

## 🔐 Authentication Model

- JWT-based stateless authentication
- Role-based access control
- Admin-only endpoints protected via dependency injection
- No server-side session storage

---

## 🧪 Automated Testing Strategy

High-signal integration tests validate:

- Atomic transfer correctness
- Idempotency guarantees
- Overdraft enforcement

Test data is provisioned programmatically via fixtures.

---

## 📂 Project Structure

app/
├── api/
├── core/
├── models/
├── services/
├── repositories/
├── db/
└── main.py

tests/
alembic/
logs/ (ignored)


---

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Pytest
- JWT (HS256)

---

## ▶️ Running the Application

```bash
uvicorn app.app:app --reload

Swagger UI:
http://127.0.0.1:8000/docs

Running Tests
pytest -v

Test logs:
logs/tests/test.log

Application logs:
logs/app/app.log

📈 Future Improvements
Event-driven audit pipeline (Kafka/SQS)
Read replicas for scaling
Distributed rate limiting
Structured JSON logging
CI/CD integration

🎯 Why This Project Matters
This project demonstrates:
Transactional integrity
Concurrency control
Financial boundary enforcement
Clean architectural separation
Production-grade logging and testing
It focuses on correctness under concurrency, which is critical in real-world backend systems.
Built with engineering rigor rather than feature quantity.
