"""Add columns for table orders

Revision ID: c8685ffebb7c
Revises: 2020d2583946
Create Date: 2025-11-21 19:43:31.043985

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c8685ffebb7c"
down_revision: Union[str, Sequence[str], None] = "2020d2583946"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "orders",
        sa.Column(
            "product_name",
            sa.String(length=255),
            nullable=False,
            comment="Название товара",
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "pickup_point_name",
            sa.String(length=100),
            nullable=False,
            comment="Имя пункта самовывоза",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("orders", "pickup_point_name")
    op.drop_column("orders", "product_name")
