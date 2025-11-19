from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.orders import PickupPoint
from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
)


class PickupPointManagerCrud:
    """
    Помощник для работы с пунктами выдачи.

    :param session: - сессия для работы с БД.

    :methods:
        - create_pickup_point: - создает новый пункт самовывоза.
        - get_pickup_point_by_name: - получает пункт самовывоза по name.
        - get_pickup_point_by_id: - получает пункт самовывоза по id.
        - get_all_pickup_points: - получает все пункты самовывоза.
        - update_pickup_point: - обновляет пункт самовывоза.
        - delete_pickup_point: - удаляет пункт самовывоза.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_pickup_point(
        self,
        pickup_point_data: PickupPointCreate,
    ) -> PickupPoint:
        """
        Создает новый пункт самовывоза.

        :param pickup_point_data: - данные для создания пункта самовывоза.
        :return: - экземпляр модели пункта самовывоза.
        """

        pickup_point = PickupPoint(**pickup_point_data.model_dump())
        self.session.add(pickup_point)
        await self.session.commit()
        return pickup_point

    async def get_pickup_point_by_name(self, name: str) -> PickupPoint | None:
        """
        Получает пункт самовывоза по name.

        :param name: - название пункта.
        :return: - экземпляр модели пункта самовывоза или None.
        """

        stmt = select(PickupPoint).filter_by(name=name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_pickup_point_by_id(self, point_id: int) -> PickupPoint | None:
        """
        Получает пункт самовывоза по name.

        :param point_id: - id пункта выдачи.
        :return: - экземпляр модели пункта самовывоза или None.
        """

        stmt = select(PickupPoint).filter_by(id=point_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_pickup_points(self) -> Sequence[PickupPoint]:
        """
        Получает все пункты самовывоза.

        :return: - список всех пунктов или None.
        """

        stmt = select(PickupPoint)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def update_pickup_point(
        self,
        pickup_point: PickupPoint,
        pickup_point_data: PickupPointUpdate,
    ) -> PickupPoint:
        """
        Обновляет пункт самовывоза.

        :param pickup_point: - экземпляр модели пункта самовывоза.
        :param pickup_point_data: - данные для обновления пункта самовывоза.
        :return: - обновленный экземпляр модели пункта самовывоза
        """

        for name, value in pickup_point_data.model_dump(exclude_unset=True).items():
            setattr(pickup_point, name, value)
        await self.session.commit()
        return pickup_point

    async def delete_pickup_point(
        self,
        pickup_point: PickupPoint,
    ) -> bool:
        """
        Удаляет пункт самовывоза.

        :param pickup_point: - экземпляр модели пункта самовывоза для удаления.
        :return: - удаление прошло успешно True.
        """

        await self.session.delete(pickup_point)
        await self.session.commit()
        return True
