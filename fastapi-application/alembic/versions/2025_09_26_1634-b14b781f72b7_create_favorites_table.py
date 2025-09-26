"""create favorites table

Revision ID: b14b781f72b7
Revises: b41edf5ac50f
Create Date: 2025-09-26 16:34:40.676098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b14b781f72b7"
down_revision: Union[str, Sequence[str], None] = "b41edf5ac50f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "favorites",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_favorites_product_id_products"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_favorites_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_favorites",
            ),
        ),
    )
    op.create_index(
        op.f("ix_favorites_product_id"),
        "favorites",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_favorites_user_id"),
        "favorites",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_favorites_user_id"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_product_id"), table_name="favorites")
    op.drop_table("favorites")
