from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr

from utils import camel_case_to_snake_case


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    """Базовая модель для всех таблиц"""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Конвертация имени таблицы"""
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    type_annotation_map = {str_256: String(256)}
