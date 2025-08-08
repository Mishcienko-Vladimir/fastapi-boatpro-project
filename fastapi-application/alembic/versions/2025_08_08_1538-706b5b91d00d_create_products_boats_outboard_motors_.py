"""Create  products, boats, outboard motors, trailers tables

Revision ID: 706b5b91d00d
Revises: cb204f959cb2
Create Date: 2025-08-08 15:38:07.929313

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "706b5b91d00d"
down_revision: Union[str, Sequence[str], None] = "cb204f959cb2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "products",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "type_product",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "name",
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_index(
        op.f("ix_products_name"),
        "products",
        ["name"],
        unique=True,
    )
    op.create_table(
        "boats",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
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
        sa.ForeignKeyConstraint(
            ["id"],
            ["products.id"],
            name=op.f("fk_boats_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_boats")),
    )
    op.create_table(
        "outboard_motors",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "engine_power",
            sa.SmallInteger(),
            nullable=False,
            comment="Мощность двигателя в л.с.",
        ),
        sa.Column(
            "company_name",
            sa.String(length=100),
            nullable=False,
            comment="Название производителя",
        ),
        sa.Column(
            "engine_type",
            sa.String(length=20),
            nullable=False,
            comment="Тип двигателя",
        ),
        sa.Column(
            "weight",
            sa.SmallInteger(),
            nullable=False,
            comment="Вес мотора в кг",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["products.id"],
            name=op.f("fk_outboard_motors_id_products"),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_outboard_motors"),
        ),
        sa.UniqueConstraint("company_name", "engine_power", name="uq_company_engine"),
    )
    op.create_table(
        "trailers",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "full_mass",
            sa.SmallInteger(),
            nullable=False,
            comment="Общая масса прицепа в кг",
        ),
        sa.Column(
            "load_capacity",
            sa.SmallInteger(),
            nullable=False,
            comment="Грузоподъемность в кг",
        ),
        sa.Column(
            "trailer_length",
            sa.SmallInteger(),
            nullable=False,
            comment="Длина прицепа в мм",
        ),
        sa.Column(
            "max_ship_length",
            sa.SmallInteger(),
            nullable=False,
            comment="Максимальная длина перевозимого судна в мм",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["products.id"],
            name=op.f("fk_trailers_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_trailers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("trailers")
    op.drop_table("outboard_motors")
    op.drop_table("boats")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
