"""create access_token table

Revision ID: ac5dbf95a737
Revises: 0f14c134bbe1
Create Date: 2025-07-07 15:03:27.278293

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac5dbf95a737'
down_revision: Union[str, Sequence[str], None] = '0f14c134bbe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'access_tokens',
        sa.Column('token', sa.String(length=43), nullable=False),
        sa.Column(
            'created_at',
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False
        ),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('fk_access_tokens_user_id_users'),
            ondelete='cascade'
        ),
        sa.PrimaryKeyConstraint('token', name=op.f('pk_access_tokens'))
    )
    op.create_index(op.f('ix_access_tokens_created_at'), 'access_tokens', ['created_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_access_tokens_created_at'), table_name='access_tokens')
    op.drop_table('access_tokens')
