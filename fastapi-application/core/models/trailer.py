from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, str_256, intpk


class Trailer(Base):
    """Таблица прицепов"""
    __tablename__ = "trailers"

    id: Mapped[intpk]
    model_name: Mapped[str_256] = mapped_column(unique=True)
    full_mass: Mapped[int]
    load_capacity: Mapped[int]
    overall_dimensions: Mapped[str_256]
    length_ship: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    image_id: Mapped[int]
