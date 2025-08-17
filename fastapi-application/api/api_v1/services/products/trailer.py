from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Trailer, ImagePath
from core.schemas.products import TrailerCreate, TrailerUpdate, TrailerRead
from core.repositories.products import ProductManagerCrud


class TrailerService:

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, Trailer)

    async def create_trailer(
        self,
        trailer_data: TrailerCreate,
        images: list[UploadFile],
    ) -> TrailerRead:
        """
        Создание нового прицепа с изображениями.
        """

        # Проверка на существование прицепа
        if await self.repo.get_product_by_name(trailer_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Trailer with name {trailer_data.name} already exists",
            )

        # Создание и сохранение прицепа с изображениями
        new_trailer = await self.repo.create_product_with_images(
            trailer_data,
            images,
        )

        # Получение прицепа с загруженными изображениями
        full_trailer = await self.repo.get_product_by_id(new_trailer.id)

        return TrailerRead.model_validate(full_trailer)

    async def get_trailer_by_name(self, name_trailer: str) -> TrailerRead:
        """
        Получение прицепа по названию.
        """

        trailer = await self.repo.get_product_by_name(name_trailer)
        if not trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with name {name_trailer} not found",
            )
        return TrailerRead.model_validate(trailer)

    async def get_trailer_by_id(self, trailer_id: int) -> TrailerRead:
        """
        Получение прицепа по id.
        """

        trailer = await self.repo.get_product_by_id(trailer_id)
        if not trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with id {trailer_id} not found",
            )
        return TrailerRead.model_validate(trailer)

    async def get_trailers(self) -> list[TrailerRead]:
        """
        Получение всех прицепов.
        """

        trailers = await self.repo.get_all_products()

        if not trailers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailers are missing",
            )
        return [TrailerRead.model_validate(trailer) for trailer in trailers]

    async def update_trailer_data_by_id(
        self,
        trailer_id: int,
        trailer_data: TrailerUpdate,
    ) -> TrailerRead:
        """
        Обновление прицепа по id, кроме изображений.
        """

        updated_trailer = await self.repo.update_product_data_by_id(
            trailer_id,
            trailer_data,
        )
        if not updated_trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with id {trailer_id} not found",
            )
        return TrailerRead.model_validate(updated_trailer)

    async def update_trailer_images_by_id(
        self,
        trailer_id: int,
        remove_images: str | None,
        add_images: list[UploadFile] | None,
    ) -> TrailerRead:
        """
        Обновление изображений прицепа по id.
        """

        if remove_images:
            remove_images_list = [
                int(item) if item.isdecimal() else None
                for item in remove_images.split(",")
            ]

            if None in remove_images_list:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"remove_images must be a list of integers or a single integer",
                )
        else:
            remove_images_list = None

        updated_trailer = await self.repo.update_product_images_by_id(
            trailer_id, remove_images_list, add_images
        )

        if not updated_trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with id {trailer_id} not found",
            )
        return TrailerRead.model_validate(updated_trailer)

    async def delete_trailer_by_id(self, trailer_id: int) -> None:
        """
        Удаление прицепа по id.
        """

        trailer = await self.repo.delete_product_by_id(trailer_id)
        if not trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with id {trailer_id} not found",
            )
        return None
