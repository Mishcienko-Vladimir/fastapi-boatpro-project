from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, str_256, intpk

class Boat(Base):
    """Таблица катеров"""
    __tablename__ = 'boats'

    id: Mapped[intpk]
    company_name: Mapped[str_256]
    model_name: Mapped[str_256] = mapped_column(unique=True)
    price: Mapped[int]
    image_id: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    length_hull: Mapped[int]
    width_hull: Mapped[int]
    weight: Mapped[int]
    capacity: Mapped[int]

    characteristics: Mapped["BoatCharacteristics"] = relationship(uselist=False, back_populates="boat")


class BoatCharacteristics(Base):
    """Таблица характеристик катеров"""
    __tablename__ = "boat_characteristics"

    id: Mapped[intpk]
    boat_id: Mapped[int] = mapped_column(ForeignKey("boats.id"), unique=True)
    maximum_load: Mapped[int]
    fuel_capacity: Mapped[int | None]
    maximum_engine_power: Mapped[int | None]
    height_side_midship: Mapped[int | None]
    transom_height: Mapped[int | None]
    hull_material: Mapped[str_256]
    thickness_side_sheet: Mapped[int]
    bottom_sheet_thickness: Mapped[int]

    boat: Mapped["Boat"] = relationship(back_populates="characteristics")
