from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Category
from core.schemas.products import CategoryCreate, CategoryRead
from core.repositories.products import ProductManagerCrud


class CategoryService:

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, Category)

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        """
        Создание новой категории.
        """
        # Проверка на существование категории
        if await self.repo.get_product_by_name(category_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category already exists",
            )

        new_category = await self.repo.create_product(category_data)
        return CategoryRead.model_validate(new_category)

    async def get_category_by_name(self, name_category: str) -> CategoryRead:
        """
        Получение категории по имени.
        """
        category = await self.repo.get_product_by_name(name_category)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with name {name_category} not found",
            )
        return CategoryRead.model_validate(category)

    async def get_category_by_id(self, category_id: int) -> CategoryRead:
        """
        Получение категории по id.
        """
        category = await self.repo.get_product_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return CategoryRead.model_validate(category)
