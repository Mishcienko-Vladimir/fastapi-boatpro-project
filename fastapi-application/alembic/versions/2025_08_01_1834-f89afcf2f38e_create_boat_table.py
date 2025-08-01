"""create boat table

Revision ID: f89afcf2f38e
Revises: 0e827ca95057
Create Date: 2025-08-01 18:34:22.805872

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f89afcf2f38e"
down_revision: Union[str, Sequence[str], None] = "0e827ca95057"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "boats",
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
            "length_hull",
            sa.SmallInteger(),
            nullable=False,
            comment="Длина корпуса в мм",
        ),
        sa.Column(
            "width_hull",
            sa.SmallInteger(),
            nullable=False,
            comment="Ширина корпуса в мм",
        ),
        sa.Column(
            "weight",
            sa.SmallInteger(),
            nullable=False,
            comment="Вес катера в кг",
        ),
        sa.Column(
            "capacity",
            sa.SmallInteger(),
            nullable=False,
            comment="Количество мест",
        ),
        sa.Column(
            "maximum_load",
            sa.SmallInteger(),
            nullable=False,
            comment="Максимальная нагрузка в кг",
        ),
        sa.Column(
            "hull_material",
            sa.String(length=50),
            nullable=False,
            comment="Материал корпуса",
        ),
        sa.Column(
            "thickness_side_sheet",
            sa.SmallInteger(),
            nullable=True,
            comment="Толщина бортового листа в мм",
        ),
        sa.Column(
            "bottom_sheet_thickness",
            sa.SmallInteger(),
            nullable=True,
            comment="Толщина днищевой листа в мм",
        ),
        sa.Column(
            "fuel_capacity",
            sa.SmallInteger(),
            nullable=True,
            comment="Объём топливного бака в литрах",
        ),
        sa.Column(
            "maximum_engine_power",
            sa.SmallInteger(),
            nullable=True,
            comment="Максимальная мощность двигателя в л.с.",
        ),
        sa.Column(
            "height_side_midship",
            sa.SmallInteger(),
            nullable=True,
            comment="Высота борта на миделе в мм",
        ),
        sa.Column(
            "transom_height",
            sa.SmallInteger(),
            nullable=True,
            comment="Высота транца в мм",
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
            name=op.f("fk_boats_type_id_product_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_boats")),
    )
    op.create_index(op.f("ix_boats_model_name"), "boats", ["model_name"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_boats_model_name"), table_name="boats")
    op.drop_table("boats")
