from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


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
