from sqlalchemy import Text, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.products import ProductBase


class Boat(ProductBase):
    """
    Таблица катеров.

    Уникальность обеспечивается по полю model_name.
    """

    model_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        comment="Модель катера",
    )
    length_hull: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Длина корпуса в мм",
    )
    width_hull: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Ширина корпуса в мм",
    )
    weight: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Вес катера в кг",
    )
    capacity: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Количество мест",
    )
    maximum_load: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Максимальная нагрузка в кг",
    )
    hull_material: Mapped[str] = mapped_column(
        String(50),
        comment="Материал корпуса",
    )
    thickness_side_sheet: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Толщина бортовой пластины в мм",
    )
    bottom_sheet_thickness: Mapped[int] = mapped_column(
        SmallInteger,
        comment="Толщина днищевой пластины в мм",
    )
    fuel_capacity: Mapped[int | None] = mapped_column(
        SmallInteger,
        comment="Ёмкость топливного бака в литрах",
    )
    maximum_engine_power: Mapped[int | None] = mapped_column(
        SmallInteger,
        comment="Максимальная мощность двигателя в л.с.",
    )
    height_side_midship: Mapped[int | None] = mapped_column(
        SmallInteger,
        comment="Высота борта на миделе в мм",
    )
    transom_height: Mapped[int | None] = mapped_column(
        SmallInteger,
        comment="Высота транца в мм",
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"model_name={self.model_name!r}, "
            f"company_name={self.company_name!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r}, "
            f"description={self.description!r}, "
            f"length_hull={self.length_hull!r}, "
            f"width_hull={self.width_hull!r}, "
            f"weight={self.weight!r}, "
            f"capacity={self.capacity!r}, "
            f"maximum_load={self.maximum_load!r}, "
            f"hull_material={self.hull_material!r}, "
            f"thickness_side_sheet={self.thickness_side_sheet!r}, "
            f"bottom_sheet_thickness={self.bottom_sheet_thickness!r}, "
            f"fuel_capacity={self.fuel_capacity!r}, "
            f"maximum_engine_power={self.maximum_engine_power!r}, "
            f"height_side_midship={self.height_side_midship!r}, "
            f"transom_height={self.transom_height!r}"
            f"type={self.type!r}, "
            f"created_at={self.created_at!r})"
        )

    def __repr__(self):
        return str(self)
