"""Create image-path table

Revision ID: cb204f959cb2
Revises: e2a6b4e9cde8
Create Date: 2025-08-07 19:19:55.714689

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb204f959cb2"
down_revision: Union[str, Sequence[str], None] = "e2a6b4e9cde8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "image_paths",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "path",
            sa.String(length=255),
            nullable=False,
            comment="Путь к изображению",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_image_paths"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("image_paths")
