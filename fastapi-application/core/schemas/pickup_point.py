from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


class PickupPointBaseModel(BaseSchemaModel):
    """
    Базовая модель для точки самовывоза.
    """

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Название пункта",
    )
    address: str = Field(
        min_length=1,
        description="Полный адрес",
    )
    work_hours: str = Field(
        min_length=1,
        max_length=100,
        description="Время работы. Пример: Пн-Пт, 9:00-19:00",
    )


class PickupPointCreate(PickupPointBaseModel):
    """
    Схемы для создания новой точки самовывоза.
    """

    pass


class PickupPointUpdate(PickupPointBaseModel):
    """
    Схемы для обновления данных о точки самовывоза.
    """

    name: Optional[str] = None
    address: Optional[str] = None
    work_hours: Optional[str] = None


class PickupPointRead(PickupPointBaseModel):
    """
    Схемы для чтения данных о точки самовывоза.
    """

    id: int = Field(
        description="ID точки самовывоза",
    )
