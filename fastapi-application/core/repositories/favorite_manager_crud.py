from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.favorite import Favorite
from core.models.products.product_base import Product
from core.schemas.favorite import FavoriteCreate


class FavoriteManagerCrud:
    """
    Помощник для работы с избранным.

    :param session: - сессия для работы с БД.

    :methods:
        - get_product_by_name - получает товар по name.
        - is_favorite_exists - проверяет, есть ли у пользователя такой товар в избранном.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_favorite(self, favorite_data: FavoriteCreate) -> Favorite:
        """
        Создает новый избранный товар.

        :param favorite_data: - данные для создания товара.
        :return: - экземпляр модели товара.
        """

        favorite = Favorite(**favorite_data.model_dump())
        self.session.add(favorite)

        await self.session.commit()
        return favorite

    async def get_favorite_with_relations(self, product_id: int) -> Favorite:
        """
        Получает избранный товар со связанными данными.

        :param product_id: - идентификатор товара.
        :return: - экземпляр модели избранного товара.
        """
        stmt = (
            select(Favorite)
            .options(
                joinedload(Favorite.product).joinedload(Product.images),
            )
            .where(Favorite.product_id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_favorites_user(self, user_id: int) -> Sequence[Favorite]:
        """
        Получает все избранные товары пользователя.

        :param user_id: ID пользователя.
        :return: Список записей Favorite.
        """
        stmt = (
            select(Favorite)
            .options(
                joinedload(Favorite.product).joinedload(Product.images),
            )
            .where(Favorite.user_id == user_id)
        )

        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def is_favorite_exists(self, user_id: int, product_id: int) -> bool:
        """
        Проверяет, есть ли у пользователя такой товар в избранном.

        :param user_id: - идентификатор пользователя.
        :param product_id: - идентификатор товара.
        :return: - True, если запись существует, иначе False.
        """

        stmt = select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def delete_favorite_by_id(self, favorite_id: int) -> bool:
        """
        Удаляет запись из избранного по id.

        :param favorite_id: ID запись избранного.
        :return: True, если удаление прошло успешно. False если избранное не найдено.
        """

        stmt = select(Favorite).where(Favorite.id == favorite_id)
        result = await self.session.execute(stmt)
        favorite = result.scalars().first()

        if not favorite:
            return False

        await self.session.delete(favorite)
        await self.session.commit()
        return True
