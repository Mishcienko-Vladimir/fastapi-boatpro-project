from sqlalchemy import UniqueConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.models.products import ProductBase


class OutboardMotor(ProductBase):
    """
    Таблица подвесных лодочных моторов.

    Уникальность модели обеспечивается по комбинации:
    - company_name
    - engine_power
    А также по полю - model_name.
    """

    __table_args__ = (
        UniqueConstraint("company_name", "engine_power", name="uq_company_engine"),
    )

    engine_power: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Мощность двигателя в л.с.",
    )
    weight: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Вес мотора в кг",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id}, "
            f"model_name={self.model_name!r},"
            f"price={self.price!r}, "
            f"company_name={self.company_name!r}, "
            f"description={self.description!r}, "
            f"images={self.images!r}, "
            f"is_active={self.is_active!r}, "
            f"engine_power={self.engine_power!r}, "
            f"weight={self.weight!r}, "
            f"type_id={self.type_id!r}, "
            f"type={self.type!r}, "
            f"created_at={self.created_at!r}, "
            f"updated_at={self.updated_at!r})"
        )

    def __repr__(self):
        return str(self)
