"""Create category table

Revision ID: e2a6b4e9cde8
Revises: ac5dbf95a737
Create Date: 2025-08-07 19:08:56.559416

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2a6b4e9cde8"
down_revision: Union[str, Sequence[str], None] = "ac5dbf95a737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=50),
            nullable=False,
            comment="Название категории",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
            comment="Описание категории",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_categories"),
        ),
    )
    op.create_index(
        op.f("ix_categories_name"),
        "categories",
        ["name"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_categories_name"),
        table_name="categories",
    )
    op.drop_table("categories")
