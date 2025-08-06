from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.image_path import ImagePath
from core.schemas import ImagePathCreate, ImagePathRead
from core.repositories.products.product_manager_crud import ProductManagerCrud


class ImagePathService:

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, ImagePath)

    async def create_image_path(self, image_path: ImagePathCreate) -> ImagePathRead:
        """
        Создание нового прицепа
        """
        # Проверка на существование типа товара
        if await self.repo.image_exists_by_path(image_path.path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image path already exists",
            )

        new_image_path = await self.repo.create_product(image_path)
        return ImagePathRead.model_validate(new_image_path)
