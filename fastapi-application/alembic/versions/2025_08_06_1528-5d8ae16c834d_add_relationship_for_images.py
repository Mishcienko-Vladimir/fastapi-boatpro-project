"""Add relationship for images

Revision ID: 5d8ae16c834d
Revises: 052243c714f8
Create Date: 2025-08-06 15:28:50.862902

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d8ae16c834d"
down_revision: Union[str, Sequence[str], None] = "052243c714f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "image_paths",
        sa.Column("trailer_id", sa.Integer(), nullable=False),
    )
    op.add_column(
        "image_paths",
        sa.Column(
            "boat_id",
            sa.Integer(),
            nullable=False,
        ),
    )
    op.add_column(
        "image_paths",
        sa.Column(
            "outboard_motor_id",
            sa.Integer(),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        op.f("fk_image_paths_boat_id_boats"),
        "image_paths",
        "boats",
        ["boat_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_image_paths_trailer_id_trailers"),
        "image_paths",
        "trailers",
        ["trailer_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_image_paths_outboard_motor_id_outboard_motors"),
        "image_paths",
        "outboard_motors",
        ["outboard_motor_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("fk_image_paths_outboard_motor_id_outboard_motors"),
        "image_paths",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_image_paths_trailer_id_trailers"),
        "image_paths",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_image_paths_boat_id_boats"),
        "image_paths",
        type_="foreignkey",
    )
    op.drop_column(
        "image_paths",
        "outboard_motor_id",
    )
    op.drop_column(
        "image_paths",
        "boat_id",
    )
    op.drop_column(
        "image_paths",
        "trailer_id",
    )
