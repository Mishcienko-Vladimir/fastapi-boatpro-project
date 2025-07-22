from sqlalchemy import Text, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin, CreatedAtMixin


class Trailer(IntIdPkMixin, CreatedAtMixin, Base):
    """Таблица прицепов"""

    model_name: Mapped[str] = mapped_column(String(100), unique=True)
    full_mass: Mapped[int] = mapped_column(SmallInteger, default=0)
    load_capacity: Mapped[int] = mapped_column(SmallInteger, default=0)
    trailer_length: Mapped[int] = mapped_column(SmallInteger, default=0)
    max_length_transported_vessel: Mapped[int] = mapped_column(SmallInteger, default=0)
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    price: Mapped[int] = mapped_column(default=0)
    image_id: Mapped[int] = mapped_column(default=0)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"model_name={self.model_name!r}, "
            f"full_mass={self.full_mass!r}, "
            f"load_capacity={self.load_capacity!r}, "
            f"trailer_length={self.trailer_length!r}, "
            f"max_length_transported_vessel={self.max_length_transported_vessel!r}, "
            f"description={self.description!r}, "
            f"price={self.price!r}, "
            f"image_id={self.image_id!r})"
        )

    def __repr__(self):
        return str(self)
