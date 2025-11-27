"""Add type product for orders table

Revision ID: eabae8491af0
Revises: 3f864dd77e19
Create Date: 2025-11-27 19:07:04.286811

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eabae8491af0"
down_revision: Union[str, Sequence[str], None] = "3f864dd77e19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "orders",
        sa.Column(
            "type_product", sa.String(length=50), nullable=False, comment="Тип товара"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("orders", "type_product")
