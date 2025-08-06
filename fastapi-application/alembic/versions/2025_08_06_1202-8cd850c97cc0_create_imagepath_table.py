"""Create ImagePath table

Revision ID: 8cd850c97cc0
Revises: 052243c714f8
Create Date: 2025-08-06 12:02:10.039594

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8cd850c97cc0"
down_revision: Union[str, Sequence[str], None] = "052243c714f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "image_paths",
        sa.Column(
            "path",
            sa.String(length=255),
            nullable=False,
            comment="Путь к изображению",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_image_paths")),
    )
    op.alter_column(
        "boats",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("boats", "image_ids")
    op.alter_column(
        "outboard_motors",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("outboard_motors", "image_ids")
    op.alter_column(
        "trailers",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("trailers", "image_ids")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "trailers",
        sa.Column(
            "image_ids",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
            comment="ID изображения",
        ),
    )
    op.alter_column(
        "trailers",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.add_column(
        "outboard_motors",
        sa.Column(
            "image_ids",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
            comment="ID изображения",
        ),
    )
    op.alter_column(
        "outboard_motors",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.add_column(
        "boats",
        sa.Column(
            "image_ids",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
            comment="ID изображения",
        ),
    )
    op.alter_column(
        "boats",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_table("image_paths")
