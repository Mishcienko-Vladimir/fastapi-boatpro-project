import logging

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.products import Trailer
from core.schemas.products import TrailerCreate, TrailerUpdate, TrailerRead
from core.repositories.products.product_manager_crud import ProductManagerCrud
from core.repositories.products.image_helper import ImageHelper


log = logging.getLogger(__name__)


class TrailerService:
    """
    Класс для управления операциями с прицепами.

    :param session: - сессия для работы с БД.

    :repo: - репозиторий (ProductManagerCrud) для работы с БД(Trailer).
    :image_helper: - вспомогательный репозиторий (ImageHelper) для работы с изображениями.

    :methods:
        - get_trailer_by_id - получение прицепа по id.
        - get_trailer_by_name - получение прицепа по названию.
        - get_trailers - получение всех прицепов.
        - create_trailer - создание нового прицепа.
        - update_trailer_data_by_id - обновление данных прицепа по id.
        - update_trailer_images_by_id - обновление изображений прицепа по id.
        - delete_trailer_by_id - удаление прицепа по id.
    """

    def __init__(self, session: AsyncSession):
        self.repo = ProductManagerCrud(session, Trailer)
        self.image_helper = ImageHelper(session)

    async def get_trailer_by_id(self, trailer_id: int) -> TrailerRead:
        """
        Получение прицепа по id.

        :trailer_id: - id прицепа.
        :return: - прицеп или 404.
        """

        trailer = await self.repo.get_product_by_id(trailer_id, options=True)
        if not trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with id {trailer_id} not found",
            )
        return trailer

    async def get_trailer_by_name(self, name_trailer: str) -> TrailerRead:
        """
        Получение прицепа по названию.

        :name_trailer: - название прицепа.
        :return: - прицеп или 404.
        """

        trailer = await self.repo.get_product_by_name(name_trailer, options=True)
        if not trailer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailer with name {name_trailer} not found",
            )
        return TrailerRead.model_validate(trailer)

    async def get_trailers(self) -> list[TrailerRead]:
        """
        Получение всех прицепов.

        :return: - список прицепов или 404.
        """

        trailers = await self.repo.get_all_products(options=True)

        if not trailers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Trailers are missing",
            )
        return [TrailerRead.model_validate(trailer) for trailer in trailers]

    async def create_trailer(
        self,
        trailer_data: TrailerCreate,
        images: list[UploadFile],
    ) -> TrailerRead:
        """
        Создание нового прицепа с изображениями.

        :param trailer_data: - данные для создания прицепа.
        :param images: - список изображений для прицепа.
        :return: - созданный прицеп или 400.
        """

        # Проверка на существование прицепа
        if await self.repo.get_product_by_name(trailer_data.name, options=True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Trailer with name {trailer_data.name} already exists",
            )

        # Создание и сохранение прицепа
        trailer = await self.repo.create_product(trailer_data)

        # Получение полной модели прицепа
        full_trailer = await self.get_trailer_by_id(trailer.id)

        # Сохранение изображений
        new_trailer = await self.image_helper.add_image_to_db(full_trailer, images)
        log.info("Created trailer: %r", new_trailer.name)

        return TrailerRead.model_validate(new_trailer)

    async def update_trailer_data_by_id(
        self,
        trailer_id: int,
        trailer_data: TrailerUpdate,
    ) -> TrailerRead:
        """
        Обновление прицепа по id, кроме изображений.

        :param trailer_id: - id прицепа.
        :param trailer_data: - данные для обновления прицепа.
        :return: - обновленный прицеп или 404.
        """

        trailer = await self.get_trailer_by_id(trailer_id)

        updated_trailer = await self.repo.update_product_data(
            trailer,
            trailer_data,
        )
        log.info("Updated trailer: %r", updated_trailer.name)

        return TrailerRead.model_validate(updated_trailer)

    async def update_trailer_images_by_id(
        self,
        trailer_id: int,
        remove_images: str | None,
        add_images: list[UploadFile],
    ) -> TrailerRead:
        """
        Обновление изображений прицепа по id.

        :param trailer_id: - id прицепа.
        :param remove_images: - строка с id изображений через запятую, которые нужно удалить.
        :param add_images: - список изображений, которые нужно добавить.
        :return: - обновленный прицеп или ошибки: 404, 422, FileNotFoundError.
        """

        trailer = await self.get_trailer_by_id(trailer_id)

        # Удаление изображений, если они переданы
        if remove_images:
            # Преобразование remove_images из строки в список int
            remove_images_list = [
                int(item) if item.isdecimal() else None
                for item in remove_images.split(",")
            ]
            if None in remove_images_list:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"remove_images must be a list of integers or a single integer",
                )
            try:
                updated_trailer = await self.image_helper.delete_image_from_db(
                    trailer,
                    remove_images_list,
                )
                # Проверка, что все изображения c id из remove_images_list были найдены в таблице
                if not updated_trailer:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Some of the images with id:{remove_images_list} are missing from the table",
                    )
                trailer = updated_trailer
            except FileNotFoundError:
                # Файлы не найдены в папке images
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Some of the images with id:{remove_images_list} are missing from the folder images",
                )

        # Добавление изображений
        updated_trailer = await self.image_helper.add_image_to_db(trailer, add_images)
        log.info("Updated trailer: %r", updated_trailer.name)

        return TrailerRead.model_validate(updated_trailer)

    async def delete_trailer_by_id(self, trailer_id: int) -> None:
        """
        Удаление прицепа по id.

        :param trailer_id: - id прицепа.
        :return: - None или ошибки: 404, FileNotFoundError.
        """

        trailer = await self.get_trailer_by_id(trailer_id)
        image_ids = [image.id for image in trailer.images]

        try:
            deleted_images = await self.image_helper.delete_image_from_db(
                trailer,
                image_ids,
            )

            # Проверка, что все изображения у trailer были найдены в таблице image_paths
            if not deleted_images:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Some of the images with id:{image_ids} are missing from the table",
                )
            trailer = deleted_images
        except FileNotFoundError:
            # Файлы не найдены в папке images
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Some of the images with id:{image_ids} are missing from the folder images",
            )

        log.info("Deleted trailer: %r", trailer.name)
        await self.repo.delete_product(trailer)
        return None
