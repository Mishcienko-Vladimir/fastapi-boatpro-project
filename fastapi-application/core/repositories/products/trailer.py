from typing import TYPE_CHECKING, Annotated, Sequence
from fastapi import Depends
from sqlalchemy import select

from core.models import db_helper
from core.models.products import Trailer
from core.schemas.products import TrailerCreate, TrailerUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class TrailerRepository:
    """
    Репозитории предназначены исключительно для взаимодействия с базой данных.

        -Работают с моделью данных (ORM).
        -Осуществляют выборку, сохранение, модификацию и удаление данных.
        -Скрывают детали работы с базой данных (типы драйверов, форматы запросов и т.д.).
        -Может включать валидацию и фильтрацию данных.
    """

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ):
        self.session = session

    async def create_trailer(self, trailer_create: TrailerCreate) -> Trailer:
        new_trailer = Trailer(**trailer_create.model_dump())
        self.session.add(new_trailer)
        await self.session.commit()
        return new_trailer

    async def get_trailer_by_id(self, trailer_id: int) -> Trailer | None:
        return await self.session.get(Trailer, trailer_id)

    async def get_all_trailers(self) -> Sequence[Trailer]:
        stmt = select(Trailer).order_by(Trailer.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_trailer(
        self,
        trailer_id: int,
        trailer_db: Trailer,
        trailer_update: TrailerUpdate,
    ) -> Trailer | None:
        trailer = await self.session.get(trailer_db, trailer_id)
        if trailer:
            for name, value in trailer_update.model_dump(exclude_unset=True).items():
                setattr(trailer, name, value)
            await self.session.commit()
            return trailer
        return None

    async def delete_trailer_by_id(
        self,
        trailer_id: int,
    ) -> bool:
        trailer = await self.session.get(Trailer, trailer_id)
        if trailer:
            await self.session.delete(trailer)
            await self.session.commit()
            return True
        return False
