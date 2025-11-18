"""Create tables orders and pickup_points

Revision ID: 2020d2583946
Revises: 31a2a31e45f6
Create Date: 2025-11-18 13:57:06.903057

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2020d2583946"
down_revision: Union[str, Sequence[str], None] = "31a2a31e45f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "pickup_points",
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
            comment="Название пункта",
        ),
        sa.Column(
            "address",
            sa.Text(),
            nullable=False,
            comment="Полный адрес",
        ),
        sa.Column(
            "work_hours",
            sa.String(length=100),
            nullable=False,
            comment="Время работы. Пример: Пн-Пт, 9:00-19:00",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_pickup_points"),
        ),
    )
    op.create_index(
        op.f("ix_pickup_points_name"),
        "pickup_points",
        ["name"],
        unique=True,
    )
    op.create_table(
        "orders",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
            comment="ID владельца заказа",
        ),
        sa.Column(
            "pickup_point_id",
            sa.Integer(),
            nullable=False,
            comment="ID пункта самовывоза",
        ),
        sa.Column(
            "product_id",
            sa.Integer(),
            nullable=False,
            comment="ID купленного товара",
        ),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "PAID",
                "CANCELLED",
                "PROCESSING",
                "READY",
                "COMPLETED",
                name="orderstatus",
            ),
            nullable=False,
            comment="Статус заказа",
        ),
        sa.Column(
            "total_price",
            sa.Integer(),
            nullable=False,
            comment="Цена на момент заказа",
        ),
        sa.Column(
            "payment_id",
            sa.String(length=255),
            nullable=True,
            comment="ID платежа в YooKassa",
        ),
        sa.Column(
            "payment_url",
            sa.String(length=500),
            nullable=True,
            comment="Ссылка для оплаты",
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="Срок действия ссылки",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Дата создания записи",
        ),
        sa.ForeignKeyConstraint(
            ["pickup_point_id"],
            ["pickup_points.id"],
            name=op.f("fk_orders_pickup_point_id_pickup_points"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_orders_product_id_products"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orders_user_id_users"),
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_orders"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders")
    op.drop_index(op.f("ix_pickup_points_name"), table_name="pickup_points")
    op.drop_table("pickup_points")
