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
    Помощник для работы с изображениями товаров.

    Отвечает за:
    - Сохранение загруженных изображений в папку `static/images` с изменением имени
    - Создание записей в таблице `ImagePath`
    - Привязку изображений к товару
    - Удаление изображений с диска и из БД

    Attributes:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def add_image_to_db(self, product, images: list[UploadFile]):
        """
        Добавляет изображения к товару, изменяет их имя и сохраняет их на диск.

        Для каждого изображения:
            1. Генерируется уникальное имя (UUID)
            2. Файл сохраняется в `static/images/`
            3. Создаётся запись в таблице `ImagePath`
            4. Изображение привязывается к товару через связь `product.images`

        Также обновляется `updated_at` у товара.

        Args:
            product: Экземпляр модели товара (Boat, Trailer и т.д.)
            images (list[UploadFile]): Список загруженных файлов изображений

        Returns:
            product: Обновлённый экземпляр товара с добавленными изображениями

        Raises:
            Exception: При ошибках записи на диск (мало места, нет прав и т.д.)

        Notes:
            - Файлы сохраняются в формате `.jpg` независимо от оригинала
            - Путь в БД хранится как `/static/images/...` (относительно корня проекта)
            - Используется `uuid4().hex` для уникальности имён
        """

        for image in images:
            # Получение пути к файлу и генерация уникального имени:
            # .../BoatPro/fastapi-application/static/images/ceb5bd3a25eb42a6a8e34cdf1ea8f5f8.jpg
            file_path = f"{settings.image_upload_dir.image_upload_dir['path']}\\{uuid4().hex}.jpg"

            # Сохранение изображений в папку .../BoatPro/fastapi-application/static/images
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
        Удаляет изображения по ID с диска и из БД.

        Для каждого ID:
            1. Проверяется, что изображение принадлежит товару
            2. Удаляется запись из `ImagePath`
            3. Удаляется файл с диска
            4. Обновляется `updated_at` у товара

        Args:
            product: Экземпляр модели товара
            remove_images (list[int]): Список ID изображений для удаления

        Returns:
            product: Обновлённый товар без удалённых изображений
            None: Если хотя бы одно изображение не найдено у товара

        Raises:
            FileNotFoundError: Если файл не найден на диске
            Exception: При ошибках удаления из БД

        Notes:
            - Удаление происходит в транзакции: если ошибка — всё откатится
            - Проверяется принадлежность изображения товару (защита от подмены ID)
            - После удаления изображение исчезает из `product.images`
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
                file_path = f"{settings.image_upload_dir.image_upload_dir['base_dir']}{image_record.path}"

                # Удаляем запись из таблицы ImagePath и из таблицы ассоциации
                product.images.remove(image_record)
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
