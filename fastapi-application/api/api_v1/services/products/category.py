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

    :param session: - сессия для работы с БД.

    :repo: - репозиторий (ProductManagerCrud) для работы с БД(Category).

    :methods:
        - get_category_by_id: - получение категории по id.
        - get_category_by_name: - получение категории по имени.
        - get_categories: - получение всех категорий.
        - create_category: - создание новой категории.
        - update_category_by_id: - обновление категории по id.
        - delete_category_by_id: - удаление категории по id.

    """

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, Category)

    async def get_category_by_id(self, category_id: int) -> CategoryRead:
        """
        Получение категории по id.

        :param category_id: - id категории.
        :return: - категория или 404.
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

        :param name_category: - имя категории.
        :return: - категория или 404.
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

        :return: - список категорий или 404.
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

        :param category_data: - данные для создания категории.
        :return: - созданная категория или 400.
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

        :param category_id: - id категории.
        :param category_data: - данные для обновления категории.
        :return: - обновленная категория или 404.
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

        :param category_id: - id категории.
        :return: - None или 404.
        """

        category = await self.get_category_by_id(category_id)

        log.info("Deleted category: %r", category.name)
        await self.repo.delete_product(category)
        return None
