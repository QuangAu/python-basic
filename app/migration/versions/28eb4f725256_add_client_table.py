"""Add Client table

Revision ID: 28eb4f725256
Revises: 7a3610e390d0
Create Date: 2024-08-29 16:05:13.248879

"""
from typing import Sequence, Union
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from common import utils


# revision identifiers, used by Alembic.
revision: str = '28eb4f725256'
down_revision: Union[str, None] = '7a3610e390d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    client_table = op.create_table('client',
    sa.Column('client_id', sa.UUID(), nullable=False),
    sa.Column('client_secret', sa.String(), nullable=False),
    sa.Column('scopes', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('client_id')
    )
    
    op.bulk_insert(client_table, [
        {
            "client_id": uuid4(),
            "client_secret": utils.hash_text("some_secret_key"), 
            "scopes": '["transfer_history"]'
        }
    ])
    

def downgrade() -> None:
    op.drop_table('client')
