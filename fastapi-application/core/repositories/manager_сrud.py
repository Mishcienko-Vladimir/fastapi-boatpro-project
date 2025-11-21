from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import (
    Type,
    TypeVar,
    Sequence,
    Generic,
    Any,
)

from core.models.base import Base


T = TypeVar("T", bound=Base)


class ManagerCrud(Generic[T]):
    """
    Универсальный CRUD-менеджер для работы с любой моделью.

    Attributes:
        session (AsyncSession): Сессия для работы с БД
        model_db (Type[T]): Модель для работы с БД

    Methods:
        create(data): - Создаёт новую запись.
        get_by_id(instance_id): - Получает запись по id.
        get_by_field(field, value): - Получает запись по полю.
        get_by_fields(**filters): - Получает запись по нескольким полям.
        get_all(): - Получает все записи.
        update(instance, data): - Обновляет запись.
        delete(instance): - Удаляет запись.
    """

    def __init__(
        self,
        session: AsyncSession,
        model_db: Type[T],
    ):
        self.session = session
        self.model_db = model_db

    async def create(self, data) -> T:
        """
        Создает новый пункт самовывоза.

        :param data: Данные для создания записи.
        :return: Экземпляр модели.
        """
        instance = self.model_db(**data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, instance_id: int) -> T | None:
        """
        Получает запись по id.

        :param instance_id: Id экземпляра.
        :return: Экземпляр модели или None.
        """
        stmt = select(self.model_db).where(self.model_db.id == instance_id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_field(self, field: str, value: Any) -> T | None:
        """
        Получает запись по любому полю.

        :param field: Название поля модели (например: "name", "email", "id").
        :param value: Значение для поиска (например: "Tom", "tom@email.com", 123).
        :raises ValueError: Если поле field не найдено в модели.
        :return: Экземпляр модели или None.
        """
        if not hasattr(self.model_db, field):
            raise ValueError(f"Модель {self.model_db.__name__} не имеет поля '{field}'")

        stmt = select(self.model_db).where(getattr(self.model_db, field) == value)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_fields(self, **filters) -> T | None:
        """
        Получает запись по нескольким полям.

        :param filters: Название полей и их значения для поиска (например: name="Tom", email="tom@email.com").
        :raises ValueError: Если поле название не найдено в модели.
        :return: Экземпляр модели или None.
        """
        stmt = select(self.model_db)
        for field, value in filters.items():
            if not hasattr(self.model_db, field):
                raise ValueError(
                    f"Модель {self.model_db.__name__} не имеет поля '{field}'"
                )
            stmt = stmt.where(getattr(self.model_db, field) == value)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> Sequence[T]:
        """
        Получает все записи.

        :return: Список всех экземпляров модели или None.
        """
        stmt = select(self.model_db)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update(self, instance: T, data) -> T:
        """
        Обновляет запись.

        :param instance: Экземпляр модели.
        :param data: Данные для обновления экземпляра.
        :return: Обновленный экземпляр модели.
        """
        for name, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, name, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: T) -> bool:
        """
        Удаляет запись.

        :param instance: Экземпляр модели для удаления.
        :return: Удаление прошло успешно True.
        """
        await self.session.delete(instance)
        await self.session.commit()
        return True
