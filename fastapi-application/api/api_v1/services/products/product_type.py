from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import ProductType
from core.schemas.products import ProductTypeCreate, ProductTypeRead
from core.repositories.products.product_manager_crud import ProductManagerCrud


class ProductTypeService:

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, ProductType)

    async def create_product_type(
        self, product_data: ProductTypeCreate
    ) -> ProductTypeRead:
        """
        Создание нового прицепа
        """
        # Проверка на существование типа товара
        if await self.repo.product_type_exists_by_name(product_data.name_product_type):
            raise HTTPException(status_code=400, detail=f"Product type already exists")

        new_product_type = await self.repo.create_product(product_data)
        return ProductTypeRead.model_validate(new_product_type)

    async def get_product_type_by_name(self, name_product_type: str) -> ProductTypeRead:
        """
        Получение типа товара по имени
        """
        product_type = await self.repo.product_type_exists_by_name(name_product_type)
        if not product_type:
            raise HTTPException(
                status_code=404,
                detail=f"Product type with name {name_product_type} not found",
            )
        return ProductTypeRead.model_validate(product_type)
