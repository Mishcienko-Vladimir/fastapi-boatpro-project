from typing import Annotated

from sqlalchemy import NullPool, String, Integer, Sm
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings


# Проверка состояние (разработка или тестирование)
if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}