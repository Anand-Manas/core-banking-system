"""Make idempotency_key nullable

Revision ID: 159bcffcc27d
Revises: 66eb711e5008
Create Date: 2026-02-10 18:23:48.833203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '159bcffcc27d'
down_revision: Union[str, Sequence[str], None] = '66eb711e5008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
