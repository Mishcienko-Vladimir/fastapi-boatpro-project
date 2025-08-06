from typing import Optional
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


class ProductTypeBaseModel(BaseSchemaModel):
    """
    Базовая схема для категории товара
    """

    name_product_type: str = Field(
        min_length=1,
        max_length=50,
        description="Название категории товара",
    )


class ProductTypeCreate(ProductTypeBaseModel):
    """
    Схемы для создания новой категории товара
    """

    pass


class ProductTypeUpdate(ProductTypeBaseModel):
    """
    Схемы для обновления данных о категории товара
    """

    name_product_type: Optional[str] = None


class ProductTypeRead(ProductTypeBaseModel):
    """
    Схемы для чтения данных о категории товара
    """

    id: int = Field(
        description="ID категории товара",
    )
    # products: list["ProductBaseModel"] = Field(
    #     description="Список товаров в категории",
    # )
