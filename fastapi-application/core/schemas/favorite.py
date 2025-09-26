from datetime import datetime
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel
from core.schemas.products.product_base_model import ProductBaseModel


class FavoriteBaseModel(BaseSchemaModel):
    """
    Базовая схема избранного товара
    """

    user_id: int = Field(
        description="ID пользователя",
    )
    product_id: int = Field(
        description="ID товара",
    )


class FavoriteCreate(FavoriteBaseModel):
    """
    Схема для создания избранного товара
    """

    pass


class FavoriteRead(FavoriteBaseModel):
    """
    Схема для чтения избранного товара
    """

    id: int = Field(
        description="ID избранного",
    )
    product: ProductBaseModel = Field(
        description="Товар",
    )
    created_at: datetime = Field(
        description="Дата добавления в избранное",
    )
