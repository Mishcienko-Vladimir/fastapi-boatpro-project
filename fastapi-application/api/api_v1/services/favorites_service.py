import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Product, ImagePath
from core.models.user import User
from core.models.favorite import Favorite

from core.schemas.user import UserFavorites
from core.schemas.favorite import FavoriteRead, FavoriteCreate

from core.repositories.products import ProductManagerCrud
from core.repositories.manager_сrud import ManagerCrud
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
        self.repo_user = ManagerCrud(session=session, model_db=User)
        self.repo = ManagerCrud(session=session, model_db=Favorite)

    async def create_favorite(self, favorite_data: FavoriteCreate) -> FavoriteRead:
        """
        Создает новый товар в избранном (с id пользователем и id товара).
        :param favorite_data: Данные для добавления в избранное.
        :return: Модель FavoriteRead с данными о добавленном товаре или ошибки 404, 400.
        """

        if not await self.repo_user.get_by_id(instance_id=favorite_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id not found",
            )

        if not await self.repo_product.get_product_by_id(
            favorite_data.product_id,
            options=True,
        ):
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

        favorite = await self.repo.create(favorite_data)
        favorite_with_relations = await self.repo.get_by_id_with_relations(
            favorite.id,
            ("product", Product),  # Favorite.product → возвращает Product
            ("images", ImagePath),  # Product.images → возвращает ImagePath
        )

        if favorite_with_relations.product.images:
            favorite_with_relations.product.image = (
                favorite_with_relations.product.images[0]
            )
        log.info("Created favorite with id: %r", favorite.id)
        return FavoriteRead.model_validate(favorite_with_relations)

    async def get_favorites(self, user_id: int) -> UserFavorites:
        """
        Получение всех избранных товаров пользователя.
        :param user_id: ID пользователя.
        :return: Все избранные товары пользователя или ошибку 404.
        """

        if not await self.repo_user.get_by_id(instance_id=user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id not found",
            )

        favorites = await self.repo_favorite.get_favorites_user(user_id)
        if not favorites:
            return UserFavorites(favorites=[])

        favorite_models = [
            FavoriteRead.model_validate(
                {
                    **favorite.__dict__,
                    "product": {
                        **favorite.product.__dict__,
                        "image": (
                            favorite.product.images[0]
                            if favorite.product.images
                            else None
                        ),
                    },
                }
            )
            for favorite in favorites
        ]
        return UserFavorites(favorites=favorite_models)

    async def delete_favorite_by_id(self, favorite_id: int) -> None:
        """
        Удаления избранного по id.

        Используется для удаление пользователем своих избранных.

        Args:
            favorite_id (int): Уникальный идентификатор избранного

        Raises:
            HTTPException: 404 NOT FOUND — Если избранное не найдено

        Returns:
            None
        """

        favorite = await self.repo.get_by_id(instance_id=favorite_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Favorite with id {favorite_id} not found",
            )
        await self.repo.delete(instance=favorite)
        return None
