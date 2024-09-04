"""Update transfer_history table

Revision ID: b1846a2af81b
Revises: 28eb4f725256
Create Date: 2024-09-04 16:45:31.173482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1846a2af81b'
down_revision: Union[str, None] = '28eb4f725256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('transfer_history', 'from_club_id',
               existing_type=sa.NUMERIC(),
               type_=sa.UUID(),
               nullable=True)


def downgrade() -> None:
   pass