from sqlalchemy import UniqueConstraint, SmallInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.products.product_base import Product


class OutboardMotor(Product):
    """
    Таблица подвесных лодочных моторов.

    Уникальность модели обеспечивается по комбинации:
    - company_name
    - engine_power
    А также по полю - name и id.
    """

    __table_args__ = (
        UniqueConstraint("company_name", "engine_power", name="uq_company_engine"),
    )

    __mapper_args__ = {"polymorphic_identity": "outboard_motor"}

    id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        primary_key=True,
        doc="Для полиморфной связи с таблицей products",
    )
    engine_power: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Мощность двигателя в л.с.",
    )
    company_name: Mapped[str] = mapped_column(
        String(100),
        comment="Название производителя",
    )
    engine_type: Mapped[str] = mapped_column(
        String(20),
        comment="Тип двигателя",
    )
    weight: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Вес мотора в кг",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"name={self.name!r}, "
            f"price={self.price!r}, "
            f"company_name={self.company_name!r}, "
            f"description={self.description!r}, "
            f"images={self.images!r}, "
            f"is_active={self.is_active!r}, "
            f"engine_power={self.engine_power!r}, "
            f"engine_type={self.engine_type!r}, "
            f"weight={self.weight!r}, "
            f"category_id={self.category_id!r}, "
            f"type_product={self.type_product!r}, "
            f"created_at={self.created_at!r}, "
            f"updated_at={self.updated_at!r})"
        )

    def __repr__(self):
        return str(self)
