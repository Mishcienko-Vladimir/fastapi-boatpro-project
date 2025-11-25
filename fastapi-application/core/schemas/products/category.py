from typing import Optional, TYPE_CHECKING
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel

if TYPE_CHECKING:
    from .boat import BoatSummarySchema  # noqa
    from .outboard_motor import OutboardMotorSummarySchema  # noqa
    from .trailer import TrailerSummarySchema  # noqa


class CategoryBaseModel(BaseSchemaModel):
    """Базовая схема для категорий товаров."""

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
    """Схема создания новой категории товара."""

    pass


class CategoryUpdate(CategoryBaseModel):
    """Схема частичного обновления категории товара."""

    name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBaseModel):
    """Схема для чтения данных категории товара."""

    id: int = Field(
        description="ID категории товара",
    )


class CategoryListBaseModel(CategoryBaseModel):
    """Базовая схема, которая используется для чтения списка товара категории."""

    products_count: int = Field(
        description="Количество товаров в категории",
    )


class CategoryListBoat(CategoryListBaseModel):
    """Схема списка всех товаров в категории катера."""

    products_preview: list["BoatSummarySchema"] = Field(
        description="Превью товаров в категории",
    )


class CategoryListOutboardMotor(CategoryListBaseModel):
    """Схема списка всех товаров в категории лодочные моторы."""

    products_preview: list["OutboardMotorSummarySchema"] = Field(
        description="Превью товаров в категории",
    )


class CategoryListTrailer(CategoryListBaseModel):
    """Схема списка всех товаров в категории прицепы."""

    products_preview: list["TrailerSummarySchema"] = Field(
        description="Превью товаров в категории",
    )
