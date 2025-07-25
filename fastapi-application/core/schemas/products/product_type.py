from typing import Optional, TYPE_CHECKING
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel

if TYPE_CHECKING:
    from .product_base_model import ProductBaseModel


class ProductTypeBaseModelModel(BaseSchemaModel):
    """
    Базовая схема для категории товара
    """

    name_product_type: str = Field(
        min_length=1,
        max_length=50,
        description="Название категории товара",
    )

