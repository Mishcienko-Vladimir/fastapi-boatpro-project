from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import Field

from .product_base_model import ProductBaseModel

if TYPE_CHECKING:
    from .product_type import ProductTypeBaseModelModel


class OutboardMotorBaseModel(ProductBaseModel):
    """
    Базовая схема для лодочных моторов
    """

    engine_power: int = Field(
        gt=0,
        lt=1000,
        description="Мощность двигателя в л.с.",
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

    model_name: Optional[str]
    price: Optional[int]
    company_name: Optional[str]
    description: Optional[str]
    image_id: Optional[int]
    is_active: Optional[bool]
    engine_power: Optional[int]
    weight: Optional[int]


class OutboardMotorRead(OutboardMotorBaseModel):
    """
    Схемы для чтения данных мотора
    """

    id: int = Field(
        description="ID мотора",
    )
    type_id: int = Field(
        description="ID категории товара",
    )
    type: "ProductTypeBaseModelModel" = Field(
        description="Категория товара",
    )
    created_at: datetime = Field(
        description="Дата создания",
    )
    updated_at: datetime = Field(
        description="Дата последнего обновления",
    )
