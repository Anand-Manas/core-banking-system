"""Make idempotency_key nullable

Revision ID: c0fb78c8afdd
Revises: 159bcffcc27d
Create Date: 2026-02-10 18:24:18.855687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0fb78c8afdd'
down_revision: Union[str, Sequence[str], None] = '159bcffcc27d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.alter_column(
        "transactions",
        "idempotency_key",
        existing_type=sa.String(),
        nullable=True
    )


def downgrade():
    op.alter_column(
        "transactions",
        "idempotency_key",
        existing_type=sa.String(),
        nullable=False
    )

