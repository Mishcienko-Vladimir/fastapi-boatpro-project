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


log = logging.getLogger(__name__)


class FavoritesService:
    """
    Сервис для управления операциями с избранным.

    Предоставляет методы для добавления, получения и удаления товаров
    в избранном у пользователя. Проверяет существование пользователя и товара,
    предотвращает дублирование. Автоматически подгружает главное изображение товара.

    Attributes:
        repo_product (ProductManagerCrud): Работа с товарами
        repo_user (ManagerCrud[User]): Проверка существования пользователя
        repo (ManagerCrud[Favorite]): Работа с избранными товарами

    Args:
        session (AsyncSession): Асинхронная сессия для работы с БД

    Methods:
        create_favorite(favorite_data): - Добавляет товар в избранное
        get_favorites(user_id): - Получает все избранные товары пользователя
        delete_favorite_by_id(favorite_id): - Удаляет избранное по ID
    """

    def __init__(self, session: AsyncSession):
        self.repo_product = ProductManagerCrud(session, Product)
        self.repo_user = ManagerCrud(session=session, model_db=User)
        self.repo = ManagerCrud(session=session, model_db=Favorite)

    async def create_favorite(self, favorite_data: FavoriteCreate) -> FavoriteRead:
        """
        Добавляет товар в избранное для пользователя.

        Проверяет:
        - Существует ли пользователь
        - Существует ли товар
        - Нет ли уже этого товара в избранном у пользователя

        После создания подгружает товар и его изображения.
        Если есть изображения — в `product.image` устанавливается первое.

        Используется при нажатии "В избранное" на странице товара.

        Args:
            favorite_data (FavoriteCreate): Схема с `user_id` и `product_id`

        Raises:
            HTTPException: 404 — Пользователь или товар не найден
            HTTPException: 400 — Товар уже в избранном

        Returns:
            FavoriteRead: Модель избранного с товаром и изображением
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

        # Проверяет, есть ли у пользователя такой товар в избранном.
        if await self.repo.get_by_fields(
            user_id=favorite_data.user_id,
            product_id=favorite_data.product_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The user already has this product in their favorites",
            )

        favorite = await self.repo.create(favorite_data)
        favorite_with_relations = await self.repo.get_all_by_field_with_relations(
            "id",
            favorite.id,
            ("product", Product),  # Favorite.product → возвращает Product
            ("images", ImagePath),  # Product.images → возвращает ImagePath
        )
        favorite_with_relations = favorite_with_relations[0]

        if favorite_with_relations.product.images:
            favorite_with_relations.product.image = (
                favorite_with_relations.product.images[0]
            )
        log.info("Created favorite with id: %r", favorite.id)
        return FavoriteRead.model_validate(favorite_with_relations)

    async def get_favorites(self, user_id: int) -> UserFavorites:
        """
        Получает все избранные товары пользователя.

        Проверяет существование пользователя.
        Подгружает товары и их изображения.
        Если у товара есть изображения — в `product.image` устанавливается первое.

        Используется на странице "Избранное".

        Args:
            user_id (int): Уникальный идентификатор пользователя

        Raises:
            HTTPException: 404 — Пользователь не найден

        Returns:
            UserFavorites: Схема с `favorites` — список из `FavoriteRead`
        """
        if not await self.repo_user.get_by_id(instance_id=user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id not found",
            )

        favorites = await self.repo.get_all_by_field_with_relations(
            "user_id",
            user_id,
            ("product", Product),  # Favorite.product → возвращает Product
            ("images", ImagePath),  # Product.images → возвращает ImagePath
        )
        if not favorites:
            return UserFavorites(favorites=[])

        favorite_models = []
        for favorite in favorites:
            if favorite.product.images:
                favorite.product.image = favorite.product.images[0]
            favorite_models.append(FavoriteRead.model_validate(favorite))

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
