from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin


class ImagePath(IntIdPkMixin, Base):
    """
    Таблица для хранения путей к изображениям.
    """

    path: Mapped[str] = mapped_column(String(255), comment="Путь к изображению")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id!r}, path={self.path!r})"

    def __repr__(self):
        return str(self)
