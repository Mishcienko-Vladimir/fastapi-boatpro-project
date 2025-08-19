import aiofiles
import logging

from aiofiles import os
from datetime import datetime, UTC
from fastapi import UploadFile
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.products import ImagePath


log = logging.getLogger(__name__)


class ImageHelper:
    """
    Помощник для работы с изображениями.

    :param session: - сессия для работы с БД.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def add_image_to_db(self, product, images: list[UploadFile]):
        """
        Добавление изображений в таблицу ImagePath и в папку images.

        :param product: - экземпляр модели товара.
        :param images: - список файлов изображений.
        :return - обновленный экземпляр товара с добавленными изображениями.
        """

        for image in images:
            # Получение пути к файлу и генерация уникального имени:
            # .../MFBoats/fastapi-application/static/images/ceb5bd3a25eb42a6a8e34cdf1ea8f5f8.jpg
            file_path = f"{settings.image_upload_dir.path}\\{uuid4().hex}.jpg"

            # Сохранение изображений в папку .../MFBoats/fastapi-application/static/images
            async with aiofiles.open(file_path, "wb") as file:
                await file.write(image.file.read())

            # Сокращаем путь до /static/images/...
            shortened_path = file_path.partition("fastapi-application")[2]

            # Создаем запись в таблицу ImagePath
            image_path = ImagePath(path=shortened_path)
            self.session.add(image_path)
            log.info("Created image: %r", shortened_path)

            # Добавляем изображение к товару
            product.images.append(image_path)

        # Обновляем время, чтобы миксин обновил updated_at
        product.updated_at = datetime.now(tz=UTC).replace(tzinfo=None)

        await self.session.commit()
        return product

    async def delete_image_from_db(self, product, remove_images: list[int]):
        """
        Удаление изображений в таблице ImagePath и в папке images.

        :param product: - экземпляр модели товара.
        :param remove_images: - список id изображений, которые нужно удалить.
        :return: - обновленный экземпляр товара с добавленными изображениями.
                 - либо None если id не найден.
                 - А также выдаёт ошибку FileNotFoundError, если файл не найден в папке images.
        """

        for image_id in remove_images:
            # Проверяем, существует ли изображения с таким id в product
            if not any(image.id == image_id for image in product.images):
                return None

        for image_id in remove_images:

            # Получаем запись из таблицы ImagePath
            stmt = select(ImagePath).filter_by(id=image_id)
            result = await self.session.execute(stmt)
            image_record = result.scalars().first()

            if image_record:
                # Получаем путь к изображению
                file_path = f"{settings.image_upload_dir.base_dir}{image_record.path}"

                # Удаляем запись из таблицы ImagePath и из таблицы ассоциации
                product.images.clear(image_record.path)
                await self.session.delete(image_record)

                # Удаляем файл с папки images
                await aiofiles.os.remove(file_path)
                log.info("Deleted image %r", file_path)

                # Обновляем время, чтобы миксин обновил updated_at
                product.updated_at = datetime.now(tz=UTC).replace(tzinfo=None)
            else:
                return None

        await self.session.commit()
        return product
