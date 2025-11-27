"""Add columns for orders table

Revision ID: 3f864dd77e19
Revises: c8685ffebb7c
Create Date: 2025-11-27 17:43:46.536375

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f864dd77e19"
down_revision: Union[str, Sequence[str], None] = "c8685ffebb7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "orders",
        sa.Column(
            "pickup_point_address",
            sa.String(length=500),
            nullable=False,
            comment="Полный адрес",
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "work_hours",
            sa.String(length=100),
            nullable=False,
            comment="Время работы. Пример: Пн-Пт, 9:00-19:00",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("orders", "work_hours")
    op.drop_column("orders", "pickup_point_address")
