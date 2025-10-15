import logging

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.products.product_manager_crud import ProductManagerCrud
from core.repositories.products.image_helper import ImageHelper


log = logging.getLogger(__name__)


class ProductsService:
    """
    Общий сервис для управления операциями с товарами (Boat, OutboardMotor, Trailer).

    :param session: - сессия для работы с БД.
    :param:product_db: - модели таблицы SQLAlchemy (Boat, OutboardMotor, Trailer, Product).

    :repo: - репозиторий (ProductManagerCrud), для работы с моделями таблицы БД (Boat, OutboardMotor, Trailer).
    :image_helper: - вспомогательный репозиторий (ImageHelper) для работы с изображениями.
    :product_db: - для указания имени таблицы в логирование: {self.product_db.__name__}.

    :methods:
        - get_product_by_id - получение товара по id.
        - get_product_by_name - получение товара по названию.
        - get_products - получение всех товаров.
        - get_search_products - получает товары по ключевому слову.
        - create_product - создание нового товара.
        - update_product_data_by_id - обновление данных товара по id.
        - update_product_images_by_id - обновление изображений товара по id.
        - delete_product_by_id - удаление товара по id.
    """

    def __init__(self, session: AsyncSession, product_db):
        self.repo = ProductManagerCrud(session, product_db)
        self.image_helper = ImageHelper(session)
        self.product_db = product_db

    async def get_product_by_id(self, product_id: int):
        """
        Получение товара по id.

        :param product_id: - id товара.
        :return: - товар (объект модели SQLAlchemy) или ошибка 404.
        """

        product = await self.repo.get_product_by_id(product_id, options=True)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product from {self.product_db.__name__} with id {product_id} not found",
            )
        return product

    async def get_product_by_name(self, product_name: str):
        """
        Получение товара по названию.

        :param product_name: - название товара.
        :return: - товар (объект модели SQLAlchemy) или ошибка 404.
        """

        product = await self.repo.get_product_by_name(product_name, options=True)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product from {self.product_db.__name__} with name {product_name} not found",
            )
        return product

    async def get_products(self):
        """
        Получение всех товаров.

        :return: - список товаров (объектов модели SQLAlchemy) или ошибка 404.
        """

        products = await self.repo.get_all_products(options=True)

        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Products in {self.product_db.__name__} are missing",
            )
        return products

    async def get_search_products(self, query: str):
        """
        Получение товаров по ключевому слову (название, производитель, описание).

        :param query: - строка для поиска.
        :return: - список товаров (объектов модели SQLAlchemy).
        """

        products = await self.repo.get_search_products(query)
        return products

    async def create_product(
        self,
        product_data,
        images: list[UploadFile],
    ):
        """
        Создание нового товара с изображениями.

        :param product_data: - данные для создания товара (pydantic схема).
        :param images: - список изображений для товара.
        :return: - созданный товар (объект модели SQLAlchemy) или ошибка 400.
        """

        # Проверка на существование товара
        if await self.repo.get_product_by_name(product_data.name, options=True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product from {self.product_db.__name__} with name {product_data.name} already exists",
            )

        # Создание и сохранение товара
        product = await self.repo.create_product(product_data)

        # Получение полной модели товара
        full_product = await self.get_product_by_id(product.id)

        # Сохранение изображений
        new_product = await self.image_helper.add_image_to_db(full_product, images)
        log.info(
            "Created product: %r in table: %r",
            new_product.name,
            self.product_db.__name__,
        )

        return new_product

    async def update_product_data_by_id(
        self,
        product_id: int,
        product_data,
    ):
        """
        Обновление товара по id, кроме изображений.

        :param product_id: - id товара.
        :param product_data: - данные для обновления товара.
        :return: - обновленный товар (объект модели SQLAlchemy) или ошибка 404.
        """

        product = await self.get_product_by_id(product_id)

        updated_product = await self.repo.update_product_data(
            product,
            product_data,
        )
        log.info(
            "Updated product: %r in table: %r",
            updated_product.name,
            self.product_db.__name__,
        )

        return updated_product

    async def update_product_images_by_id(
        self,
        product_id: int,
        remove_images: str | None,
        add_images: list[UploadFile],
    ):
        """
        Обновление изображений товара по id.

        :param product_id: - id товара.
        :param remove_images: - строка с id изображений (через запятую), которые нужно удалить.
        :param add_images: - список изображений, которые нужно добавить.
        :return: - обновленный товар (объект модели SQLAlchemy) или ошибки: 404, 422, FileNotFoundError.
        """

        product = await self.get_product_by_id(product_id)

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
                updated_product = await self.image_helper.delete_image_from_db(
                    product,
                    remove_images_list,
                )
                # Проверка, что все изображения c id из remove_images_list были найдены в таблицах
                if not updated_product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Some of the images with id:{remove_images_list} "
                        f"are missing from the table {self.product_db.__name__} or the table image_paths",
                    )
                product = updated_product
            except FileNotFoundError:
                # Файлы не найдены в папке images
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Some of the images with id:{remove_images_list} are missing from the folder images",
                )

        # Добавление изображений
        updated_product = await self.image_helper.add_image_to_db(product, add_images)
        log.info(
            "Updated product: %r in table: %r",
            updated_product.name,
            self.product_db.__name__,
        )

        return updated_product

    async def delete_product_by_id(self, product_id: int) -> None:
        """
        Удаление товара по id.

        :param product_id: - id товара.
        :return: - None или ошибки: 404, FileNotFoundError.
        """

        product = await self.get_product_by_id(product_id)
        image_ids = [image.id for image in product.images]

        try:
            deleted_images = await self.image_helper.delete_image_from_db(
                product,
                image_ids,
            )

            # Проверка, что все изображения у product были найдены в таблице image_paths
            if not deleted_images:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Some of the images with id:{image_ids} are missing from the table image_paths",
                )
            product = deleted_images
        except FileNotFoundError:
            # Файлы не найдены в папке images
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Some of the images with id:{image_ids} are missing from the folder images",
            )

        log.info(
            "Deleted product: %r in table: %r",
            product.name,
            self.product_db.__name__,
        )
        await self.repo.delete_product(product)
        return None
