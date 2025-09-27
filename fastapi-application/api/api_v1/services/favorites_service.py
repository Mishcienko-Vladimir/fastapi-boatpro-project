import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Product
from core.schemas.favorite import FavoriteRead, FavoriteCreate
from core.repositories.products import ProductManagerCrud
from core.repositories.user_manager_crud import UserManagerCrud
from core.repositories.favorite_manager_crud import FavoriteManagerCrud


log = logging.getLogger(__name__)


class FavoritesService:
    """
    Сервис для управления операциями с избранным.

    :param session: - сессия для работы с БД.

    :repo_product: - репозиторий (ProductManagerCrud) для работы с БД(Product).
    :repo_favorite: - репозиторий (FavoriteManagerCrud) для работы с БД(Favorite).
    :repo_user: - репозиторий (UserManagerCrud) для работы с БД(User).

    :methods:
        - add_favorite: - добавляет пользователю товар в избранное.
    """

    def __init__(self, session: AsyncSession):
        self.repo_product = ProductManagerCrud(session, Product)
        self.repo_favorite = FavoriteManagerCrud(session)
        self.repo_user = UserManagerCrud(session)

    async def create_favorite(self, favorite_data: FavoriteCreate) -> FavoriteRead:
        """
        Создает новый товар в избранном (с id пользователем и id товара).
        :param favorite_data: Данные для добавления в избранное.
        :return: Модель FavoriteRead с данными о добавленном товаре или ошибки 404, 400.
        """

        user = await self.repo_user.get_user_by_id(favorite_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id not found",
            )

        product = await self.repo_product.get_product_by_id(
            favorite_data.product_id, options=True
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {favorite_data.product_id} not found",
            )

        if await self.repo_favorite.is_favorite_exists(
            favorite_data.user_id,
            favorite_data.product_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The user already has this product in their favorites",
            )

        favorite = await self.repo_favorite.create_favorite(favorite_data)
        favorite_with_relations = await self.repo_favorite.get_favorite_with_relations(
            favorite.product_id,
        )
        log.info("Created favorite with id: %r", favorite.id)

        return FavoriteRead.model_validate(favorite_with_relations)
