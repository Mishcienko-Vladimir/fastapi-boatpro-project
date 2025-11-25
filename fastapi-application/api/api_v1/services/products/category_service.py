import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Category
from core.schemas.products import CategoryCreate, CategoryRead, CategoryUpdate
from core.repositories.products import ProductManagerCrud


log = logging.getLogger(__name__)


class CategoryService:
    """
    Класс для управления операциями с категориями.

    Attributes:
        repo (ProductManagerCrud): Репозиторий для работы с моделью Category в БД

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД

    Methods:
        get_category_by_id: - Получение категории по ID
        get_category_by_name: - Получение категории по имени
        get_categories: - Получение всех категорий
        create_category: - Создание новой категории
        update_category_by_id: - Обновление категории по ID
        delete_category_by_id: - Удаление категории по ID
    """

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, Category)

    async def get_category_by_id(self, category_id: int) -> CategoryRead:
        """
        Получение категории по id.

        Используется при отображении конкретной категории, например, в админ-панели.

        Args:
            category_id (int): Уникальный идентификатор категории

        Raises:
            HTTPException: 404 NOT FOUND — Если категория с указанным ID не найдена

        Returns:
            CategoryRead: Модель категории, готовая к возврату через API
        """

        category = await self.repo.get_product_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return category

    async def get_category_by_name(self, name_category: str) -> CategoryRead:
        """
        Получение категории по имени.

        Используется при проверке уникальности имени при создании или обновлении.

        Args:
            name_category (str): Название категории (например, "Лодки")

        Raises:
            HTTPException: 404 NOT FOUND — Если категория с таким именем не найдена

        Returns:
            CategoryRead: Модель категории, готовая к возврату через API
        """

        category = await self.repo.get_product_by_name(name_category)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with name {name_category} not found",
            )
        return CategoryRead.model_validate(category)

    async def get_categories(self) -> list[CategoryRead]:
        """
        Получение всех категорий.

        Используется в админ-панели и при загрузке фильтров на фронтенде.

        Raises:
            HTTPException: 404 NOT FOUND — Если в системе нет ни одной категории

        Returns:
            list[CategoryRead]: Список категорий, готовых к возврату через API
        """

        categories = await self.repo.get_all_products()
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categories are missing",
            )
        return [CategoryRead.model_validate(category) for category in categories]

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        """
        Создание новой категории.

        Используется в админ-панели для добавления новых типов товаров.

        Args:
            category_data (CategoryCreate): Схема с данными для создания категории

        Raises:
            HTTPException: 400 BAD REQUEST — Если категория с таким именем уже существует

        Returns:
            CategoryRead: Модель созданной категории
        """

        # Проверка на существование категории
        if await self.repo.get_product_by_name(category_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with name {category_data.name} already exists",
            )

        new_category = await self.repo.create_product(category_data)
        log.info("Created category: %r", new_category.name)

        return CategoryRead.model_validate(new_category)

    async def update_category_by_id(
        self,
        category_id: int,
        category_data: CategoryUpdate,
    ) -> CategoryRead:
        """
        Обновление категории по id.

        Используется в админ-панели при редактировании категории.

        Args:
            category_id (int): Уникальный идентификатор категории
            category_data (CategoryUpdate): Схема с новыми данными (опционально)

        Raises:
            HTTPException: 404 NOT FOUND — Если категория не найдена

        Returns:
            CategoryRead: Обновлённая модель категории
        """

        category = await self.get_category_by_id(category_id)

        updated_category = await self.repo.update_product_data(
            category,
            category_data,
        )
        log.info("Updated category: %r", updated_category.name)

        return CategoryRead.model_validate(updated_category)

    async def delete_category_by_id(self, category_id: int) -> None:
        """
        Удаление категории по id.

        Используется в админ-панели при удалении категории.

        Args:
            category_id (int): Уникальный идентификатор категории

        Raises:
            HTTPException: 404 NOT FOUND — Если категория не найдена

        Returns:
            None
        """

        category = await self.get_category_by_id(category_id)

        log.info("Deleted category: %r", category.name)
        await self.repo.delete_product(category)
        return None
