import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
    PickupPointRead,
)
from core.repositories.pickup_point_manager_crud import PickupPointManagerCrud


log = logging.getLogger(__name__)


class PickupPointsService:
    """
    Сервис для управления операциями с пунктом выдачи.

    :param session: - сессия для работы с БД.

    :methods:
        - get_pickup_point_by_id: - получение пункта выдачи по id.
        - get_pickup_point_by_name: - получение пункта выдачи по имени.
        - get_pickup_points: - получение всех пунктов выдачи.
        - create_pickup_point: - создание нового пункта выдачи.
        - update_pickup_point_by_id: - обновление пункта выдачи по id.
        - delete_pickup_point_by_id: - удаление пункта выдачи по id.
    """

    def __init__(self, session: AsyncSession):
        self.repo = PickupPointManagerCrud(session=session)

    async def get_pickup_point_by_id(self, pickup_point_id: int):
        """
        Получение пункта выдачи по id.

        :param pickup_point_id: - id пункта выдачи.
        :return: - пункт выдачи или 404.
        """

        pickup_point = await self.repo.get_pickup_point_by_id(pickup_point_id)
        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pickup point with id {pickup_point_id} not found",
            )
        return pickup_point

    async def get_pickup_point_by_name(self, pickup_point_name: str) -> PickupPointRead:
        """
        Получение пункта выдачи по имени.

        :param pickup_point_name: - имя пункта выдачи.
        :return: - пункт выдачи или 404.
        """

        pickup_point = await self.repo.get_pickup_point_by_name(pickup_point_name)
        if not pickup_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pickup point with name {pickup_point_name} not found",
            )
        return PickupPointRead.model_validate(pickup_point)

    async def get_pickup_points(self) -> list[PickupPointRead]:
        """
        Получение всех пунктов выдачи.

        :return: - список пунктов выдачи или 404.
        """

        pickup_points = await self.repo.get_all_pickup_points()
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
        Создание нового пункта выдачи.

        :param pickup_point_data: - данные для создания пункта выдачи.
        :return: - созданный пункт выдачи или 400.
        """

        # Проверка на существование категории
        if await self.repo.get_pickup_point_by_name(pickup_point_data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pickup point with name {pickup_point_data.name} already exists",
            )

        new_pickup_point = await self.repo.create_pickup_point(pickup_point_data)
        log.info("Created pickup point: %r", new_pickup_point.name)

        return PickupPointRead.model_validate(new_pickup_point)

    async def update_pickup_point_by_id(
        self,
        pickup_point_id: int,
        pickup_point_data: PickupPointUpdate,
    ) -> PickupPointRead:
        """
        Обновление пункта выдачи по id.

        :param pickup_point_id: - id пункта выдачи.
        :param pickup_point_data: - данные для обновления пункта выдачи.
        :return: - обновленный пункт выдачи или 404.
        """

        pickup_point = await self.get_pickup_point_by_id(pickup_point_id)

        updated_pickup_point = await self.repo.update_pickup_point(
            pickup_point,
            pickup_point_data,
        )
        log.info("Updated pickup_point: %r", updated_pickup_point.name)

        return PickupPointRead.model_validate(updated_pickup_point)

    async def delete_pickup_point_by_id(self, pickup_point_id: int) -> None:
        """
        Удаление пункта выдачи по id.

        :param pickup_point_id: - id пункта выдачи.
        :return: - None или 404.
        """

        pickup_point = await self.get_pickup_point_by_id(pickup_point_id)

        log.info("Deleted pickup point: %r", pickup_point.name)
        await self.repo.delete_pickup_point(pickup_point)
        return None
