from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, str_256

class Boats(Base):
    """Таблица катеров"""
    __tablename__ = 'boats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str_256]
    model_name: Mapped[str_256] = mapped_column(unique=True)
    price: Mapped[int]
    image_id: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    length_hull: Mapped[int]
    width_hull: Mapped[int]
    weight: Mapped[int]
    capacity: Mapped[int]
    fuel_capacity: Mapped[int | None]
    engine_power: Mapped[int | None]
    hull_material: Mapped[str_256]


class OutboardMotor(Base):
    """Таблица подвесных лодочных моторов"""
    __tablename__ = 'outboard motor'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str_256]
    engine_power: Mapped[int]
    price: Mapped[int]
    weight: Mapped[int]
    description: Mapped[str] = mapped_column(Text)


class Trailer(Base):
    """Таблица прицепов"""
    __tablename__ = 'trailer'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_name: Mapped[str_256] = mapped_column(unique=True)
    full_mass: Mapped[int]
    load_capacity: Mapped[int]
    overall_dimensions: Mapped[str_256]
    length_ship: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]



