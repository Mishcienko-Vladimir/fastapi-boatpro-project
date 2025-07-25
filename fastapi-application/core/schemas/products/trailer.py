from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import Field

from .product_base_model import ProductBaseModel

if TYPE_CHECKING:
    from .product_type import ProductTypeBaseModelModel


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
        description="Длина прицепа в мм",
    )
    max_ship_length: int = Field(
        gt=0,
        lt=32767,
        description="Максимальная длина перевозимого судна в мм",
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

    model_name: Optional[str]
    price: Optional[int]
    company_name: Optional[str]
    description: Optional[str]
    image_id: Optional[int]
    is_active: Optional[bool]
    full_mass: Optional[int]
    load_capacity: Optional[int]
    trailer_length: Optional[int]
    max_ship_length: Optional[int]


class TrailerRead(TrailerBaseModel):
    """
    Схемы для чтения данных прицепа
    """

    id: int = Field(
        description="ID прицепа",
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
