from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from .boat import BoatSummarySchema


class CategoryBaseModel(BaseSchemaModel):
    """
    Базовая схема для категории товара
    """

    name: str = Field(
        min_length=1,
        max_length=50,
        description="Название категории товара",
    )
    description: str | None = Field(
        min_length=0,
        description="Описание категории",
    )


class CategoryCreate(CategoryBaseModel):
    """
    Схемы для создания новой категории товара
    """

    pass


class CategoryUpdate(CategoryBaseModel):
    """
    Схемы для обновления данных о категории товара
    """

    name_product_type: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBaseModel):
    """
    Схемы для чтения данных о категории товара
    """

    id: int = Field(
        description="ID категории товара",
    )


class CategoryListBoat(CategoryBaseModel):
    """
    Список всех товаров в категории катера и их количество.
    """

    products_count: int = Field(
        description="Количество товаров в категории",
    )
    products_preview: list[BoatSummarySchema] = Field(
        description="Превью товаров в категории",
    )
