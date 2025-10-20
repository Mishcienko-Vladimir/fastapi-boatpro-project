"""add new colums for outboard motors table

Revision ID: 31a2a31e45f6
Revises: b14b781f72b7
Create Date: 2025-10-10 18:11:55.594892

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "31a2a31e45f6"
down_revision: Union[str, Sequence[str], None] = "b14b781f72b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "outboard_motors",
        sa.Column(
            "number_cylinders",
            sa.SmallInteger(),
            nullable=False,
            comment="Количество цилиндров в двигателе",
        ),
    )
    op.add_column(
        "outboard_motors",
        sa.Column(
            "engine_displacement",
            sa.SmallInteger(),
            nullable=False,
            comment="Объем двигателя в куб.см",
        ),
    )
    op.add_column(
        "outboard_motors",
        sa.Column(
            "control_type",
            sa.String(length=20),
            nullable=False,
            comment="Тип управления",
        ),
    )
    op.add_column(
        "outboard_motors",
        sa.Column(
            "starter_type", sa.String(length=20), nullable=False, comment="Тип стартера"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("outboard_motors", "starter_type")
    op.drop_column("outboard_motors", "control_type")
    op.drop_column("outboard_motors", "engine_displacement")
    op.drop_column("outboard_motors", "number_cylinders")
