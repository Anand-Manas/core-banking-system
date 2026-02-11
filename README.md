# Core Banking System Backend

A production-grade backend system built using FastAPI.

## Features

- JWT Authentication (Admin & Customer roles)
- Controlled Overdraft Enforcement
- Atomic Money Transfers with Row-Level Locking
- Per-Customer Idempotency
- Redis Cache-Aside Strategy
- Audit Logging for Sensitive Operations
- High-Signal Automated Tests

## Tech Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Alembic
- Pytest

## How to Run

```bash
uvicorn app.main:app --reload
