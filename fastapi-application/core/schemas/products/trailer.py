from datetime import datetime
from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from .product_base_model import ProductBaseModel
from .image_path import ImagePathRead
from .category import CategoryRead


class TrailerBaseModel(ProductBaseModel):
    """
    Базовая схема для прицепа
    """

    full_mass: int = Field(
        gt=0,
        lt=32767,
        description="Полный вес прицепа в кг",
    )
    load_capacity: int = Field(
        gt=0,
        lt=32767,
        description="Грузоподъемность в кг",
    )
    trailer_length: int = Field(
        gt=0,
        lt=32767,
        description="Длина прицепа в см",
    )
    max_ship_length: int = Field(
        gt=0,
        lt=32767,
        description="Максимальная длина перевозимого судна в см",
    )


class TrailerCreate(TrailerBaseModel):
    """
    Схемы для создания нового прицепа
    """

    pass


class TrailerUpdate(TrailerBaseModel):
    """
    Схемы для обновления данных прицепа
    """

    name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    full_mass: Optional[int] = None
    load_capacity: Optional[int] = None
    trailer_length: Optional[int] = None
    max_ship_length: Optional[int] = None


class TrailerRead(TrailerBaseModel):
    """
    Схемы для чтения данных прицепа
    """

    id: int = Field(
        description="ID прицепа",
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


class TrailerSummarySchema(BaseSchemaModel):
    """
    Краткая информация о прицепе.
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
    full_mass: int = Field(
        gt=0,
        lt=32767,
        description="Полный вес прицепа в кг",
    )
    max_ship_length: int = Field(
        gt=0,
        lt=32767,
        description="Максимальная длина перевозимого судна в см",
    )
    image: ImagePathRead = Field(
        description="Главное изображение",
    )
