"""Add relationship

Revision ID: e2af50a0ddcc
Revises: 706b5b91d00d
Create Date: 2025-08-08 15:45:45.286608

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e2af50a0ddcc"
down_revision: Union[str, Sequence[str], None] = "706b5b91d00d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "product_images",
        sa.Column(
            "product_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "image_id",
            sa.Integer(),
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
    op.add_column(
        "products",
        sa.Column("category_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_products_category_id_categories"),
        "products",
        "categories",
        ["category_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("fk_products_category_id_categories"),
        "products",
        type_="foreignkey",
    )
    op.drop_column(
        "products",
        "category_id",
    )
    op.drop_table("product_images")
