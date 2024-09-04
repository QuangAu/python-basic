"""insert root user

Revision ID: 7a3610e390d0
Revises: 60d4fa6c8607
Create Date: 2024-08-29 11:34:37.753637

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a3610e390d0'
down_revision: Union[str, None] = '60d4fa6c8607'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    user = sa.table('user',
        sa.column('id', sa.UUID),
        sa.column('name', sa.String),
        sa.column('login_id', sa.String),
        sa.column('password', sa.String),
        sa.column('is_admin', sa.Boolean),
        sa.column('is_active', sa.Boolean)
    )
    
    data = {
        'id': uuid4(),
        'name': 'root',
        'password': '$2b$12$6qACznq6ftyF5gS7OgxgEOykZWds4AUCGN/OQdjDmU5oQRiWXE3bi',
        'login_id': 'root',
        'is_admin': True,
        'is_active': True
    }
    
    session.execute(sa.insert(user).values(data))


def downgrade() -> None:
    pass
