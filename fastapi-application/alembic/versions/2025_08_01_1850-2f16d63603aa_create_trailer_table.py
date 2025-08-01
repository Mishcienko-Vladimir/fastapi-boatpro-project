"""create trailer table

Revision ID: 2f16d63603aa
Revises: c856398ed84e
Create Date: 2025-08-01 18:50:01.411734

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f16d63603aa"
down_revision: Union[str, Sequence[str], None] = "c856398ed84e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "trailers",
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
            name=op.f("fk_trailers_type_id_product_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_trailers")),
    )
    op.create_index(
        op.f("ix_trailers_model_name"), "trailers", ["model_name"], unique=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_trailers_model_name"), table_name="trailers")
    op.drop_table("trailers")
