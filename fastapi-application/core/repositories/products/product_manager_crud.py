from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from sqlalchemy import select

from core.models import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ProductManagerCrud:
    """
    Помощник для работы с товарами.
    """

    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        product_db,
        product_create,
        product_update,
    ):
        self.session = session
        self.product_db = product_db
        self.product_create = product_create
        self.product_update = product_update

    async def create_product(self):
        """
        Создает новый товар.
        """

        new_product = self.product_db(**self.product_create.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        return new_product

    async def get_product_by_id(self, product_id: int):
        """
        Получает товар по ID.
        """

        return await self.session.get(self.product_db, product_id)

    async def get_all_product(self):
        """
        Получает все товары.
        """

        stmt = select(self.product_db).order_by(self.product_db.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_product(self, product_id: int):
        """
        Обновляет товар по ID.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            for name, value in self.product_update.model_dump(
                exclude_unset=True
            ).items():
                setattr(product, name, value)
            await self.session.commit()
            return product
        return None

    async def delete_product(self, product_id: int) -> bool:
        """
        Удаляет товар по ID.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()
            return True
        return False
