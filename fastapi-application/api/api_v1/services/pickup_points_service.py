import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.orders.pickup_point import PickupPoint
from core.repositories.manager_сrud import ManagerCrud
from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
    PickupPointRead,
)


log = logging.getLogger(__name__)


class PickupPointsService:
    """
    Сервис для управления операциями с пунктами самовывоза.

    Предоставляет методы для создания, получения, обновления и удаления
    пунктов самовывоза. Использует универсальный репозиторий `ManagerCrud`
    для взаимодействия с базой данных.

    Attributes:
        repo (ManagerCrud): Репозиторий для работы с моделью PickupPoint в БД

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД

    Methods:
        get_pickup_point_by_id(pickup_point_id): - Получение пункта по ID
        get_pickup_point_by_name(pickup_point_name): - Получение по имени
        get_pickup_points(): - Получение всех пунктов
        create_pickup_point(pickup_point_data): - Создание нового пункта
        update_pickup_point_by_id(pickup_point_id, pickup_point_data): - Обновление
        delete_pickup_point_by_id(pickup_point_id): - Удаление пункта
    """

    def __init__(self, session: AsyncSession):
        self.repo = ManagerCrud(session=session, model_db=PickupPoint)

    async def get_pickup_point_by_id(self, pickup_point_id: int):
        """
        Получает пункт самовывоза по его уникальному идентификатору.

        Используется при оформлении заказа и в админ-панели.

        Args:
            pickup_point_id (int): Уникальный идентификатор пункта самовывоза

        Raises:
            HTTPException: 404 NOT FOUND — Если пункт с указанным ID не найден

        Returns:
            PickupPoint: SQLAlchemy-модель (не Pydantic-схема)
        """

        pickup_point = await self.repo.get_by_id(instance_id=pickup_point_id)
        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pickup point with id {pickup_point_id} not found",
            )
        return pickup_point

    async def get_pickup_point_by_name(self, pickup_point_name: str) -> PickupPointRead:
        """
        Получает пункт самовывоза по его названию.

        Используется при валидации уникальности при создании и в интерфейсах выбора пункта.

        Args:
            pickup_point_name (str): Название пункта самовывоза

        Raises:
            HTTPException: 404 NOT FOUND — Если пункт с таким именем не найден
            ValueError: Если поле `name` отсутствует в модели

        Returns:
            PickupPointRead: Модель найденного пункта самовывоза
        """

        pickup_points = await self.repo.get_by_fields(
            field="name",
            value=pickup_point_name,
        )
        pickup_point = pickup_points[0] if pickup_points else None
        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pickup point with name {pickup_point_name} not found",
            )
        return PickupPointRead.model_validate(pickup_point)

    async def get_pickup_points(self) -> list[PickupPointRead]:
        """
        Получает все доступные пункты самовывоза в системе.

        Используется в интерфейсе оформления заказа и в админ-панели.

        Raises:
            HTTPException: 404 NOT FOUND — Если в системе нет ни одного пункта

        Returns:
            list[PickupPointRead]: Список всех пунктов самовывоза
        """

        pickup_points = await self.repo.get_all()
        if not pickup_points:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pickup points are missing",
            )
        return [
            PickupPointRead.model_validate(pickup_point)
            for pickup_point in pickup_points
        ]

    async def create_pickup_point(
        self,
        pickup_point_data: PickupPointCreate,
    ) -> PickupPointRead:
        """
        Создаёт новый пункт самовывоза.

        Используется в админ-панели для добавления новых точек выдачи.

        Args:
            pickup_point_data (PickupPointCreate): Схема с `name`, `address`, `work_hours`

        Raises:
            HTTPException: 400 BAD REQUEST — Если имя уже занято
            HTTPException: 422 UNPROCESSABLE ENTITY — Если данные не прошли валидацию

        Returns:
            PickupPointRead: Модель созданного пункта самовывоза
        """

        # Проверка на существование пункта выдачи с таким же именем
        if await self.repo.get_by_fields(
            field="name",
            value=pickup_point_data.name,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pickup point with name {pickup_point_data.name} already exists",
            )

        new_pickup_point = await self.repo.create(data=pickup_point_data)
        log.info("Created pickup point with name: %r", new_pickup_point.name)
        return PickupPointRead.model_validate(new_pickup_point)

    async def update_pickup_point_by_id(
        self,
        pickup_point_id: int,
        pickup_point_data: PickupPointUpdate,
    ) -> PickupPointRead:
        """
        Обновляет данные пункта самовывоза по его ID.

        Позволяет частично обновить поля: `name`, `address`, `work_hours`.
        Если поле не передано — оно не изменяется. Проверяется существование
        пункта. Используется в админ-панели.

        Args:
            pickup_point_id (int): Уникальный идентификатор пункта
            pickup_point_data (PickupPointUpdate): Схема с опциональными полями

        Raises:
            HTTPException: 404 NOT FOUND — Если пункт не найден

        Returns:
            PickupPointRead: Обновлённая модель пункта самовывоза
        """

        pickup_point = await self.get_pickup_point_by_id(
            pickup_point_id=pickup_point_id
        )

        updated_pickup_point = await self.repo.update(
            instance=pickup_point,
            data=pickup_point_data,
        )
        log.info("Updated pickup_point with id: %r", pickup_point_id)
        return PickupPointRead.model_validate(updated_pickup_point)

    async def delete_pickup_point_by_id(self, pickup_point_id: int) -> None:
        """
        Удаляет пункт самовывоза по его ID.

        Используется в админ-панели. Удаление каскадно не затрагивает заказы.

        Args:
            pickup_point_id (int): Уникальный идентификатор пункта

        Raises:
            HTTPException: 404 NOT FOUND — Если пункт не найден

        Returns:
            None
        """

        pickup_point = await self.get_pickup_point_by_id(
            pickup_point_id=pickup_point_id
        )

        log.info("Deleted pickup point with id: %r", pickup_point_id)
        await self.repo.delete(instance=pickup_point)
        return None
