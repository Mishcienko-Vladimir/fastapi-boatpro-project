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

    model_name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    image_id: Optional[int] = None
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
