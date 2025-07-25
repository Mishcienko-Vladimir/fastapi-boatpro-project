from datetime import datetime
from typing import Optional
from pydantic import Field

from core.schemas.base import BaseSchema


class TrailerBase(BaseSchema):
    """
    Базовая схема для прицепа
    """

    model_name: str = Field(
        min_length=1,
        max_length=255,
        description="Название модели прицепа",
    )
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
    description: str = Field(
        min_length=0,
        description="Описание прицепа",
    )
    price: int = Field(
        gt=0,
        description="Цена прицепа в рублях",
    )
    image_id: list[int] = Field(
        description="ID изображения прицепа",
    )


class TrailerCreate(TrailerBase):
    """
    Схемы для создания нового прицепа
    """

    pass


class TrailerUpdate(TrailerBase):
    """
    Схемы для обновления данных прицепа
    """

    model_name: Optional[str]
    full_mass: Optional[int]
    load_capacity: Optional[int]
    trailer_length: Optional[int]
    max_ship_length: Optional[int]
    description: Optional[str]
    price: Optional[int]
    image_id: Optional[int]


class TrailerRead(TrailerBase):
    """
    Схемы для чтения данных прицепа
    """

    id: int = Field(description="ID прицепа")
    created_at: datetime = Field(description="Дата создания")
    updated_at: datetime = Field(description="Дата последнего обновления")
