from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base
from core.models.mixins import IntIdPkMixin


class ImagePath(IntIdPkMixin, Base):
    """
    Таблица для хранения путей к изображениям.
    """

    path: Mapped[str] = mapped_column(String(255), comment="Путь к изображению")

    def __str__(self):
        return f"{self.__class__.__name__}" f"(id={self.id!r}, " f"path='{self.path}')"

    def __repr__(self):
        return str(self)
