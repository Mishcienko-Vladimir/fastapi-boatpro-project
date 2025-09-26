from datetime import datetime
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from core.schemas.products.product_base_model import ProductBaseModel


class FavoriteModel(BaseSchemaModel):
    """
    Схема избранного товара
    """

    id: int = Field(
        description="ID избранного",
    )
    product: ProductBaseModel = Field(
        description="Продукт",
    )
    created_at: datetime = Field(
        description="Дата добавления в избранное",
    )
