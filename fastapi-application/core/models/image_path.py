from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin


class ImagePath(IntIdPkMixin, Base):
    """
    Таблица для хранения путей к изображениям.
    """

    path: Mapped[str] = mapped_column(String(255), comment="Путь к изображению")

    trailer_id: Mapped[int | None] = mapped_column(ForeignKey("trailers.id"))
    boat_id: Mapped[int | None] = mapped_column(ForeignKey("boats.id"))
    outboard_motor_id: Mapped[int | None] = mapped_column(
        ForeignKey("outboard_motors.id")
    )

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id!r}, path={self.path!r})"

    def __repr__(self):
        return str(self)
