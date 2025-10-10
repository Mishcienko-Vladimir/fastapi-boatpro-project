from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from .product_base_model import ProductBaseModel
from .image_path import ImagePathRead
from .category import CategoryRead


class EngineType(str, Enum):
    """
    Типы двигателей.
    """

    two_stroke = "двухтактный"
    four_stroke = "четырехтактный"


class ControlType(str, Enum):
    """
    Типы управления.
    """

    tiller_control = "румпельное"
    remote_control = "дистанционное"


class StarterType(str, Enum):
    """
    Типы стартера.
    """

    manual_starter = "ручной"
    electric_starter = "электрический"


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
    number_cylinders: int = Field(
        gt=0,
        lt=100,
        description="Количество цилиндров в двигателе",
    )
    engine_displacement: int = Field(
        gt=0,
        lt=10000,
        description="Объем двигателя в куб.см",
    )
    control_type: ControlType = Field(
        description="Тип управления",
    )
    starter_type: StarterType = Field(
        description="Тип стартера",
    )


class OutboardMotorCreate(OutboardMotorBaseModel):
    """
    Схема для создания нового мотора
    """

    category_id: int = Field(
        description="ID категории товара",
    )


class OutboardMotorUpdate(OutboardMotorBaseModel):
    """
    Схема для обновления дынных мотора
    """

    name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    engine_power: Optional[int] = None
    engine_type: Optional[EngineType] = None
    weight: Optional[int] = None
    number_cylinders: Optional[int] = None
    engine_displacement: Optional[int] = None
    control_type: Optional[ControlType] = None
    starter_type: Optional[StarterType] = None


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
    images: list[ImagePathRead] = Field(
        description="Список изображений",
    )


class OutboardMotorSummarySchema(BaseSchemaModel):
    """
    Краткая информация о лодочном моторе.
    """

    id: int = Field(
        description="ID товара",
    )
    name: str = Field(
        min_length=1,
        max_length=255,
        description="Название модели",
    )
    price: int = Field(
        gt=0,
        description="Цена в рублях",
    )
    company_name: str = Field(
        min_length=1,
        max_length=100,
        description="Название производителя",
    )
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
    engine_type: EngineType = Field(
        description="Тип двигателя",
    )
    engine_displacement: int = Field(
        gt=0,
        lt=10000,
        description="Объем двигателя в куб.см",
    )
    control_type: ControlType = Field(
        description="Тип управления",
    )
    starter_type: StarterType = Field(
        description="Тип стартера",
    )
    is_active: bool = Field(
        description="Наличие товара",
    )
    image: Optional[ImagePathRead] = Field(
        None,
        description="Главное изображение",
    )
