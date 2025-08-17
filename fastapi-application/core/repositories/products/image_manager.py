import aiofiles
from aiofiles import os

from fastapi import HTTPException, status, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from core.config import settings
from core.models.products import ImagePath


class ImageManager:
    """
    Помощник для работы с изображениями.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def add_image_to_db(self, product, images: list[UploadFile]):
        """
        Добавление изображений в таблицу ImagePath и в папку images.

        :param product - экземпляр модели товара.
        :param images - список файлов изображений.
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

            # Добавляем изображение к товару
            product.images.append(image_path)

        await self.session.commit()
        return product
