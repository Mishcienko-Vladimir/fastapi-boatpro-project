from typing import Optional
from datetime import datetime
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from .image_path import ImagePathRead


class ProductBaseModel(BaseSchemaModel):
    """
    Базовая модель для товаров.
    """

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
    description: str = Field(
        min_length=0,
        description="Описание",
    )
    is_active: bool = Field(
        description="Наличие товара",
    )


class ProductBaseModelCreate(ProductBaseModel):
    """Базовая модель для создания товаров."""

    category_id: int = Field(
        description="ID категории товара",
    )


class ProductBaseModelUpdate(ProductBaseModel):
    """
    Базовая модель для обновления товаров.
    """

    name: Optional[str] = None
    price: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ProductBaseModelRead(ProductBaseModel):
    """
    Базовая модель для чтения товаров.
    """

    id: int = Field(
        description="ID товара",
    )
    type_product: str = Field(
        description="Тип товара",
    )
    created_at: datetime = Field(
        description="Дата создания",
    )
    updated_at: datetime = Field(
        description="Дата последнего обновления",
    )
    image: Optional[ImagePathRead] = None
