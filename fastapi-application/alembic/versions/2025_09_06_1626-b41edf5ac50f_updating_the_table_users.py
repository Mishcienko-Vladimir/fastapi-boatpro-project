"""Updating the table users

Revision ID: b41edf5ac50f
Revises: 05f031db8cb3
Create Date: 2025-09-06 16:26:11.411947

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b41edf5ac50f"
down_revision: Union[str, Sequence[str], None] = "05f031db8cb3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "first_name",
            sa.String(length=50),
            nullable=False,
            comment="Имя пользователя",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "first_name")
