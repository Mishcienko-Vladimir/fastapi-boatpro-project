from typing import Annotated

from sqlalchemy import String, MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr

from core.config import settings
from utils import camel_case_to_snake_case


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    """Базовая модель для всех таблиц"""
    __abstract__ = True

    # Для имен миграций
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Конвертация имени таблицы"""
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    type_annotation_map = {str_256: String(256)}
