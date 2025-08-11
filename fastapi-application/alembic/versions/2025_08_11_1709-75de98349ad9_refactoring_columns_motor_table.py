"""Refactoring columns motor table

Revision ID: 75de98349ad9
Revises: e2af50a0ddcc
Create Date: 2025-08-11 17:09:26.075779

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "75de98349ad9"
down_revision: Union[str, Sequence[str], None] = "e2af50a0ddcc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "boats",
        "length_hull",
        existing_type=sa.SMALLINT(),
        comment="Длина корпуса в см",
        existing_comment="Длина корпуса в мм",
        existing_nullable=False,
    )
    op.alter_column(
        "boats",
        "width_hull",
        existing_type=sa.SMALLINT(),
        comment="Ширина корпуса в см",
        existing_comment="Ширина корпуса в мм",
        existing_nullable=False,
    )
    op.drop_constraint(
        op.f("uq_company_engine"),
        "outboard_motors",
        type_="unique",
    )
    op.drop_column("outboard_motors", "company_name")
    op.alter_column(
        "trailers",
        "trailer_length",
        existing_type=sa.SMALLINT(),
        comment="Длина прицепа в см",
        existing_comment="Длина прицепа в мм",
        existing_nullable=False,
    )
    op.alter_column(
        "trailers",
        "max_ship_length",
        existing_type=sa.SMALLINT(),
        comment="Максимальная длина перевозимого судна в см",
        existing_comment="Максимальная длина перевозимого судна в мм",
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "trailers",
        "max_ship_length",
        existing_type=sa.SMALLINT(),
        comment="Максимальная длина перевозимого судна в мм",
        existing_comment="Максимальная длина перевозимого судна в см",
        existing_nullable=False,
    )
    op.alter_column(
        "trailers",
        "trailer_length",
        existing_type=sa.SMALLINT(),
        comment="Длина прицепа в мм",
        existing_comment="Длина прицепа в см",
        existing_nullable=False,
    )
    op.add_column(
        "outboard_motors",
        sa.Column(
            "company_name",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
            comment="Название производителя",
        ),
    )
    op.create_unique_constraint(
        op.f("uq_company_engine"),
        "outboard_motors",
        ["company_name", "engine_power"],
        postgresql_nulls_not_distinct=False,
    )
    op.alter_column(
        "boats",
        "width_hull",
        existing_type=sa.SMALLINT(),
        comment="Ширина корпуса в мм",
        existing_comment="Ширина корпуса в см",
        existing_nullable=False,
    )
    op.alter_column(
        "boats",
        "length_hull",
        existing_type=sa.SMALLINT(),
        comment="Длина корпуса в мм",
        existing_comment="Длина корпуса в см",
        existing_nullable=False,
    )
