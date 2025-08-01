"""create product type table

Revision ID: 0e827ca95057
Revises: ac5dbf95a737
Create Date: 2025-08-01 18:21:02.340732

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e827ca95057"
down_revision: Union[str, Sequence[str], None] = "ac5dbf95a737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "product_types",
        sa.Column("name_product_type", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_types")),
    )
    op.create_index(
        op.f("ix_product_types_name_product_type"),
        "product_types",
        ["name_product_type"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_product_types_name_product_type"), table_name="product_types"
    )
    op.drop_table("product_types")
