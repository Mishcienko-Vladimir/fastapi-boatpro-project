from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import Field

from .product_base_model import ProductBaseModel
from .image_path import ImageRead
from .category import CategoryRead


class EngineType(str, Enum):
    """
    Типы двигателей
    """

    two_stroke = "двухтактный"
    four_stroke = "четырехтактный"


class OutboardMotorBaseModel(ProductBaseModel):
    """
    Базовая схема для лодочных моторов.
    """

    engine_power: int = Field(
        gt=0,
        lt=1000,
        description="Мощность двигателя в л.с.",
    )
    engine_type: EngineType = Field(
        description="Тип двигателя",
    )
    weight: int = Field(
        gt=0,
        lt=1000,
        description="Вес мотора в кг",
    )


class OutboardMotorCreate(OutboardMotorBaseModel):
    """
    Схема для создания нового мотора
    """

    pass


class OutboardMotorUpdate(OutboardMotorBaseModel):
    """
    Схема для обновления дынных мотора
    """

    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    engine_power: Optional[int] = None
    engine_type: Optional[EngineType] = None
    weight: Optional[int] = None


class OutboardMotorRead(OutboardMotorBaseModel):
    """
    Схемы для чтения данных мотора
    """

    id: int = Field(
        description="ID мотора",
    )
    category: CategoryRead = Field(
        description="Категория",
    )
    created_at: datetime = Field(
        description="Дата создания",
    )
    updated_at: datetime = Field(
        description="Дата последнего обновления",
    )
    images: list[ImageRead] = Field(
        description="Список изображений",
    )
