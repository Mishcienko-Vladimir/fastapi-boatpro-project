"""Add relationship in product type and product base tables

Revision ID: 052243c714f8
Revises: 2f16d63603aa
Create Date: 2025-08-04 17:35:35.643856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "052243c714f8"
down_revision: Union[str, Sequence[str], None] = "2f16d63603aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "boats",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "outboard_motors",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "trailers",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "trailers",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "outboard_motors",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "boats",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
