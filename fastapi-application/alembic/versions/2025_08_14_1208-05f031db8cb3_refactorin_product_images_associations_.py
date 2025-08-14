"""Refactorin product-images-associations table

Revision ID: 05f031db8cb3
Revises: 75de98349ad9
Create Date: 2025-08-14 12:08:56.168550

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05f031db8cb3"
down_revision: Union[str, Sequence[str], None] = "75de98349ad9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "product_images_associations",
        sa.Column(
            "product_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "image_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["image_id"],
            ["image_paths.id"],
            name=op.f("fk_product_images_associations_image_id_image_paths"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_product_images_associations_product_id_products"),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_product_images_associations"),
        ),
    )
    op.drop_table("product_images")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "product_images",
        sa.Column(
            "product_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "image_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["image_id"],
            ["image_paths.id"],
            name=op.f("fk_product_images_image_id_image_paths"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_product_images_product_id_products"),
        ),
    )
    op.drop_table("product_images_associations")
