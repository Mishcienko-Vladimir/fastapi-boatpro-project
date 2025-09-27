from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.favorite import Favorite
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
            .options(joinedload(Favorite.product))
            .where(Favorite.product_id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

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
