from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


class ProductManagerCrud:
    """
    Универсальный CRUD-менеджер для работы с товарами (Boat, Trailer, OutboardMotor и др.).

    Предоставляет базовые операции: создание, чтение, обновление, удаление.
    Поддерживает работу с любыми моделями товаров, унаследованными от `ProductBase`.
    Автоматически подгружает связанные данные: категорию и изображения.

    Attributes:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД
        product_db: Модель товара (например: Boat, Trailer, OutboardMotor)

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
        product_db: Конкретная модель товара (например: Boat)

    Methods:
        get_product_by_name(name, options): - Получает товар по имени.
        get_product_by_id(product_id, options): - Получает товар по ID.
        get_all_products(options): - Получает все товары.
        get_search_products(query): - Ищет товары по названию, производителю или описанию.
        create_product(product_data): - Создаёт новый товар.
        update_product_data(product, product_data): - Обновляет данные товара (без изображений).
        delete_product(product): - Удаляет товар из БД.
    """

    def __init__(
        self,
        session: AsyncSession,
        product_db,
    ):
        self.session = session
        self.product_db = product_db

    async def get_product_by_name(self, name: str, options: bool = None):
        """
         Получает товар по его названию.

        Args:
            name (str): Название товара (полное или частичное)
            options (bool): Если True — подгружает связанные данные:
                           - Категорию (category)
                           - Изображения (images)

        Returns:
            Экземпляр модели товара или None, если не найден

        """

        stmt = select(self.product_db).filter_by(name=name)
        if options:
            stmt = stmt.options(
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int, options: bool = None):
        """
        Получает товар по его уникальному идентификатору.

        Args:
            product_id (int): Уникальный ID товара
            options (bool): Если True — подгружает связанные данные:
                           - Категорию (category)
                           - Изображения (images)

        Returns:
            Экземпляр модели товара или None, если не найден

        """

        stmt = select(self.product_db).filter_by(id=product_id)
        if options:
            stmt = stmt.options(
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_products(self, options: bool = None):
        """
        Получает все товары указанного типа (например, все катера).

        Args:
            options (bool): Если True — подгружает связанные данные:
                           - Категорию (category)
                           - Изображения (images)

        Returns:
            Список всех товаров (может быть пустым)

        """

        stmt = select(self.product_db)
        if options:
            stmt = stmt.options(
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_search_products(self, query: str):
        """
        Выполняет поиск товаров по ключевому слову.

        Ищет совпадения в:
        - Названии товара
        - Названии производителя
        - Описании товара

        Args:
            query (str): Ключевое слово для поиска

        Returns:
            Список товаров, соответствующих запросу

        """

        stmt = (
            select(self.product_db)
            .where(
                (self.product_db.name.ilike(f"%{query}%"))
                | (self.product_db.company_name.ilike(f"%{query}%"))
                | (self.product_db.description.ilike(f"%{query}%")),
            )
            .options(
                selectinload(self.product_db.category),
                selectinload(self.product_db.images),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def create_product(self, product_data):
        """
        Создаёт новый товар в базе данных.

        Args:
            product_data: Pydantic-схема с данными для создания товара

        Returns:
            Созданный экземпляр модели товара с заполненным `id`

        """

        product = self.product_db(**product_data.model_dump())
        self.session.add(product)

        await self.session.commit()
        return product

    async def update_product_data(self, product, product_data):
        """
        Обновляет данные товара (без обработки изображений).

        Поддерживает частичное обновление (только переданные поля).

        Args:
            product: Существующий экземпляр товара
            product_data: Pydantic-схема с новыми данными

        Returns:
            Обновлённый экземпляр модели

        """

        for name, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, name, value)
        await self.session.commit()
        return product

    async def delete_product(self, product) -> bool:
        """
        Удаляет товар из базы данных.

        Args:
            product: Экземпляр товара, который нужно удалить

        Returns:
            bool: True, если удаление прошло успешно
        """

        await self.session.delete(product)
        await self.session.commit()
        return True
