"""create outboard motor table

Revision ID: c856398ed84e
Revises: f89afcf2f38e
Create Date: 2025-08-01 18:43:32.134242

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c856398ed84e"
down_revision: Union[str, Sequence[str], None] = "f89afcf2f38e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "outboard_motors",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "model_name",
            sa.String(length=255),
            nullable=False,
            comment="Название модели",
        ),
        sa.Column(
            "price",
            sa.Integer(),
            nullable=False,
            comment="Цена в рублях",
        ),
        sa.Column(
            "company_name",
            sa.String(length=100),
            nullable=False,
            comment="Название производителя",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            comment="Описание",
        ),
        sa.Column(
            "image_ids",
            sa.JSON(),
            nullable=False,
            comment="ID изображения",
        ),
        sa.Column(
            "engine_power",
            sa.SmallInteger(),
            nullable=False,
            comment="Мощность двигателя в л.с.",
        ),
        sa.Column(
            "weight",
            sa.SmallInteger(),
            nullable=False,
            comment="Вес мотора в кг",
        ),
        sa.Column(
            "type_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            comment="Наличие товара",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Последнее обновление записи",
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["product_types.id"],
            name=op.f("fk_outboard_motors_type_id_product_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_outboard_motors")),
        sa.UniqueConstraint("company_name", "engine_power", name="uq_company_engine"),
    )
    op.create_index(
        op.f("ix_outboard_motors_model_name"),
        "outboard_motors",
        ["model_name"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_outboard_motors_model_name"), table_name="outboard_motors")
    op.drop_table("outboard_motors")
