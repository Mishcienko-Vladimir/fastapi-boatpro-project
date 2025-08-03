from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


class ProductManagerCrud:
    """
    Помощник для работы с товарами.
    """

    def __init__(
        self,
        session: AsyncSession,
        product_db,
    ):
        self.session = session
        self.product_db = product_db

    async def create_product(self, product_data):
        """
        Создает новый товар.
        """

        new_product = self.product_db(**product_data.model_dump())
        self.session.add(new_product)
        await self.session.commit()
        return new_product

    async def product_type_exists_by_name(self, name) -> bool:
        """
        Проверяет, существует ли тип товара с заданным именем.
        """

        stmt = select(self.product_db).filter_by(name_product_type=name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_name(self, model_name: str):
        """
        Найдет товар по model_name.
        """

        stmt = select(self.product_db).filter_by(model_name=model_name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int):
        """
        Получает товар по id.
        """

        return await self.session.get(self.product_db, product_id)

    async def get_all_products(self):
        """
        Получает все товары.
        """

        stmt = select(self.product_db).order_by(self.product_db.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def update_product(self, product_update_schema, product_id: int):
        """
        Обновляет товар по id.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            for name, value in product_update_schema.model_dump(
                exclude_unset=True
            ).items():
                setattr(product, name, value)
            await self.session.commit()
            return product
        return None

    # async def delete_product(self, product_id: int) -> bool:
    #     """
    #     Удаляет товар по id.
    #     """
    #
    #     product = await self.get_product_by_id(product_id)
    #     if product:
    #         await self.session.delete(product)
    #         await self.session.commit()
    #         return True
    #     return False
