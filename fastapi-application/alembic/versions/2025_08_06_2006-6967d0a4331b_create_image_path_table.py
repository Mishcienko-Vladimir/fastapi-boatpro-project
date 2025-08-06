"""Create image path table

Revision ID: 6967d0a4331b
Revises: 5d8ae16c834d
Create Date: 2025-08-06 20:06:39.124873

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6967d0a4331b"
down_revision: Union[str, Sequence[str], None] = "5d8ae16c834d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "image_paths",
        sa.Column(
            "path", sa.String(length=255), nullable=False, comment="Путь к изображению"
        ),
        sa.Column("trailer_id", sa.Integer(), nullable=False),
        sa.Column("boat_id", sa.Integer(), nullable=False),
        sa.Column("outboard_motor_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["boat_id"],
            ["boats.id"],
            name=op.f("fk_image_paths_boat_id_boats"),
        ),
        sa.ForeignKeyConstraint(
            ["outboard_motor_id"],
            ["outboard_motors.id"],
            name=op.f("fk_image_paths_outboard_motor_id_outboard_motors"),
        ),
        sa.ForeignKeyConstraint(
            ["trailer_id"],
            ["trailers.id"],
            name=op.f("fk_image_paths_trailer_id_trailers"),
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
    op.drop_column(
        "outboard_motors",
        "image_ids",
    )
    op.alter_column(
        "trailers",
        "type_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column(
        "trailers",
        "image_ids",
    )


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
