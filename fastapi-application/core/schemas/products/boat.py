from datetime import datetime
from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from .product_base_model import ProductBaseModel
from .image_path import ImageRead
from .category import CategoryRead


class BoatBaseModel(ProductBaseModel):
    """
    Базовая схема для катеров.
    """

    length_hull: int = Field(
        gt=0,
        lt=30000,
        description="Длина корпуса в см",
    )
    width_hull: int = Field(
        gt=0,
        lt=10000,
        description="Ширина корпуса в см",
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

    category_id: Optional[int] = None
    name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
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


class BoatRead(BoatBaseModel):
    """
    Схемы для чтения данных катера
    """

    id: int = Field(
        description="ID катера",
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


class BoatSummarySchema(BaseSchemaModel):
    """
    Краткая информация о катере.
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
    length_hull: int = Field(
        gt=0,
        lt=30000,
        description="Длина корпуса в см",
    )
    width_hull: int = Field(
        gt=0,
        lt=10000,
        description="Ширина корпуса в см",
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
    image: ImageRead = Field(
        description="Главное изображение",
    )
