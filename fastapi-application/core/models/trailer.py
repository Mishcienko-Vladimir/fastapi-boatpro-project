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

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"model_name={self.model_name!r}, "
            f"full_mass={self.full_mass!r}, "
            f"load_capacity={self.load_capacity!r}, "
            f"overall_dimensions={self.overall_dimensions!r}, "
            f"length_ship={self.length_ship!r}, "
            f"description={self.description!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r})"
        )

    def __repr__(self):
        return str(self)
