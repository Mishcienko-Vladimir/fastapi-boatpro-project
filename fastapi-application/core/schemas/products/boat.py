from datetime import datetime
from typing import Optional
from pydantic import Field

from .product_base_model import ProductBaseModel
from .product_type import ProductTypeRead


class BoatBaseModel(ProductBaseModel):
    """
    Базовая схема для катеров
    """

    length_hull: int = Field(
        gt=0,
        lt=30000,
        description="Длина корпуса в мм",
    )
    width_hull: int = Field(
        gt=0,
        lt=10000,
        description="Ширина корпуса в мм",
    )
    weight: int = Field(
        gt=0,
        lt=32767,
        description="Вес катера в кг",
    )
    capacity: int = Field(
        gt=0,
        lt=100,
        description="Количество мест",
    )
    maximum_load: int = Field(
        gt=0,
        lt=5000,
        description="Максимальная нагрузка в кг",
    )
    hull_material: str = Field(
        min_length=1,
        max_length=50,
        description="Материал корпуса",
    )
    thickness_side_sheet: int | None = Field(
        ge=0,
        lt=1000,
        description="Толщина бортового листа в мм",
    )
    bottom_sheet_thickness: int | None = Field(
        ge=0,
        lt=1000,
        description="Толщина днищевой листа в мм",
    )
    fuel_capacity: int | None = Field(
        ge=0,
        lt=1000,
        description="Объём топливного бака в литрах",
    )
    maximum_engine_power: int | None = Field(
        ge=0,
        lt=10000,
        description="Максимальная мощность двигателя в л.с.",
    )
    height_side_midship: int | None = Field(
        ge=0,
        lt=10000,
        description="Высота борта на миделе в мм",
    )
    transom_height: int | None = Field(
        ge=0,
        lt=1000,
        description="Высота транца в мм",
    )


class BoatCreate(BoatBaseModel):
    """
    Схема для создания нового катера
    """

    pass


class BoatUpdate(BoatBaseModel):
    """
    Схема для обновления дынных катера
    """

    model_name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    image_id: Optional[int] = None
    is_active: Optional[bool] = None
    length_hull: Optional[int] = None
    width_hull: Optional[int] = None
    weight: Optional[int] = None
    capacity: Optional[int] = None
    maximum_load: Optional[int] = None
    hull_material: Optional[str] = None
    thickness_side_sheet: Optional[int] = None
    bottom_sheet_thickness: Optional[int] = None
    fuel_capacity: Optional[int] = None
    maximum_engine_power: Optional[int] = None
    height_side_midship: Optional[int] = None
    transom_height: Optional[int] = None
    type_id: Optional[int] = None


class BoatRead(BoatBaseModel):
    """
    Схемы для чтения данных катера
    """

    id: int = Field(
        description="ID катера",
    )
    type: ProductTypeRead = Field(
        description="Категория товара",
    )
    created_at: datetime = Field(
        description="Дата создания",
    )
    updated_at: datetime = Field(
        description="Дата последнего обновления",
    )
