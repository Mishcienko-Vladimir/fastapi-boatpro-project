from typing import Annotated

from sqlalchemy import NullPool, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# from core.config import settings
#
#
# engine = create_async_engine(url=settings.DATABASE_URL)
#
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}