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

    :param session: - сессия для работы с БД.
    :param model_db: - модель для работы с БД.

    :methods:
        - create: - создает новую запись.
        - get_by_id: - получает запись по id.
        - get_by_field: - получает запись по полю.
        - get_by_fields: - получает запись по нескольким полям.
        - get_all: - получает все записи.
        - update: - обновляет запись.
        - delete: - удаляет запись.
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

        :param data: - данные для создания записи.
        :return: - экземпляр модели.
        """
        instance = self.model_db(**data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, instance_id: int) -> T | None:
        """
        Получает запись по id.

        :param instance_id: - id экземпляра.
        :return: - экземпляр модели или None.
        """
        stmt = select(self.model_db).where(self.model_db.id == instance_id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_field(self, field: str, value: Any) -> T | None:
        """
        Получает запись по любому полю.

        :param field: - название поля модели (например: "name", "email", "id").
        :param value: - значение для поиска (например: "Tom", "tom@email.com", 123).
        :raises ValueError: - если поле field не найдено в модели.
        :return: - экземпляр модели или None.
        """
        if not hasattr(self.model_db, field):
            raise ValueError(f"Модель {self.model_db.__name__} не имеет поля '{field}'")

        stmt = select(self.model_db).where(getattr(self.model_db, field) == value)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_fields(self, **filters) -> T | None:
        """
        Получает запись по нескольким полям.

        :param filters: - название полей и их значения для поиска (например: name="Tom", email="tom@email.com").
        :raises ValueError: - если поле название не найдено в модели.
        :return: - экземпляр модели или None.
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

        :return: - список всех экземпляров модели или None.
        """
        stmt = select(self.model_db)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update(self, instance: T, data) -> T:
        """
        Обновляет запись.

        :param instance: - экземпляр модели.
        :param data: - данные для обновления экземпляра.
        :return: - обновленный экземпляр модели.
        """
        for name, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, name, value)
        await self.session.commit()
        return instance

    async def delete(self, instance: T) -> bool:
        """
        Удаляет запись.

        :param instance: - экземпляр модели для удаления.
        :return: - удаление прошло успешно True.
        """
        await self.session.delete(instance)
        await self.session.commit()
        return True
