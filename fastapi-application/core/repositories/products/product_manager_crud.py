import aiofiles
from aiofiles import os

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


from core.config import settings
from core.models.products import ImagePath
from core.repositories.products.image_manager import ImageManager


class ProductManagerCrud:
    """
    Помощник для работы с товарами.
    """

    def __init__(
        self,
        session: AsyncSession,
        product_db,
    ):
        self.session = session
        self.product_db = product_db  # Тип модели SQLAlchemy (Boat, Trailer и т.д.)

    async def create_product_with_images(self, product_data, images):
        """
        Создает новый товар с изображением.
        """

        product = self.product_db(**product_data.model_dump())
        self.session.add(product)

        _service = ImageManager(self.session)
        new_product = await _service.add_image_to_db(product, images)

        await self.session.commit()
        return new_product

    async def get_product_by_name(self, name: str):
        """
        Найдет товар по name.
        """

        stmt = (
            select(self.product_db)
            .filter_by(name=name)
            .options(
                joinedload(self.product_db.category),
                joinedload(self.product_db.images),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int):
        """
        Получает товар по id.
        """

        stmt = (
            select(self.product_db)
            .filter_by(id=product_id)
            .options(
                joinedload(self.product_db.category),
                joinedload(self.product_db.images),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_products(self):
        """
        Получает все товары.
        """

        stmt = select(self.product_db).options(
            joinedload(self.product_db.category),
            joinedload(self.product_db.images),
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update_product_data_by_id(
        self,
        product_id: int,
        product_update_schema,
    ):
        """
        Обновляет товар по id, без обработки изображений.
        """

        product = await self.get_product_by_id(product_id)

        if product:
            for name, value in product_update_schema.model_dump(
                exclude_unset=True
            ).items():
                setattr(product, name, value)
            await self.session.commit()
            return product
        return None

    async def update_product_images_by_id(
        self,
        product_id: int,
        remove_images_list,
        add_images,
    ):
        product = await self.get_product_by_id(product_id)

        if not product:
            return None

        if remove_images_list:
            # Удаление изображений с диска
            for image in remove_images_list:
                # Удаление записи из ImagePath
                stmt = select(ImagePath).filter_by(id=image)
                result = await self.session.execute(stmt)
                image_record = result.scalars().first()

                # Получаем путь к изображению
                file_path = f"{settings.image_upload_dir.base_dir}{image_record.path}"
                product.images.clear(image_record.path)

                if image_record:
                    await self.session.delete(image_record)

                try:
                    # Удаляем файл с диска
                    await aiofiles.os.remove(file_path)
                except FileNotFoundError:
                    # Файл не найден — можно логировать ошибку
                    print(f"Файл {file_path} не найден.")

        # Если есть новые изображения, сохраняем их
        if add_images:
            for image in add_images:
                file_path = f"{settings.image_upload_dir.path}\\{uuid4().hex}.jpg"

                # Сохранение изображений в папку .../MFBoats/fastapi-application/static/images
                async with aiofiles.open(file_path, "wb") as file:
                    await file.write(image.file.read())

                # Сокращаем путь до /static/images/...
                shortened_path = file_path.partition("fastapi-application")[2]

                # Создаем запись в таблицу ImagePath
                image_path = ImagePath(path=shortened_path)
                self.session.add(image_path)

                # Добавляем изображение к прицепу
                product.images.append(image_path)
        await self.session.commit()
        return product

    async def delete_product_by_id(self, product_id: int) -> bool:
        """
        Удаляет товар по id.
        """

        product = await self.get_product_by_id(product_id)

        if product:
            # Получаем список связанных изображений
            related_images = list(product.images)

            # Удаление изображений с диска
            for image in related_images:
                # Получаем путь к изображению
                file_path = f"{settings.image_upload_dir.base_dir}{image.path}"

                # Удаление записи из ImagePath
                stmt = select(ImagePath).filter_by(id=image.id)
                result = await self.session.execute(stmt)
                image_record = result.scalars().first()

                if image_record:
                    await self.session.delete(image_record)

                try:
                    # Удаляем файл с диска
                    await aiofiles.os.remove(file_path)
                except FileNotFoundError:
                    # Файл не найден — можно логировать ошибку
                    print(f"Файл {file_path} не найден.")

            await self.session.delete(product)
            await self.session.commit()
            return True
        return False

    async def create_category(self, category_data):
        """
        Создает новую категорию.
        """

        new_category = self.product_db(**category_data.model_dump())
        self.session.add(new_category)
        await self.session.commit()
        return new_category

    async def get_category_by_name(self, name: str):
        """
        Найдет категорию по name.
        """

        stmt = select(self.product_db).filter_by(name=name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_category_by_id(self, product_id: int):
        """
        Получает категорию по id.
        """

        stmt = select(self.product_db).filter_by(id=product_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_category(self):
        """
        Получает все категории.
        """

        stmt = select(self.product_db)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update_category_by_id(
        self,
        product_id: int,
        product_update_schema,
    ):
        """
        Обновляет категория по id.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            for name, value in product_update_schema.model_dump(
                exclude_unset=True
            ).items():
                setattr(product, name, value)
            await self.session.commit()
            return product
        return None

    async def delete_category_by_id(self, product_id: int) -> bool:
        """
        Удаляет товар по id.
        """

        product = await self.get_product_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()
            return True
        return False
