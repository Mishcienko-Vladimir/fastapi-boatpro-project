from typing import Optional, TYPE_CHECKING
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel

if TYPE_CHECKING:
    from .boat import BoatSummarySchema  # noqa
    from .outboard_motor import OutboardMotorSummarySchema  # noqa
    from .trailer import TrailerSummarySchema  # noqa


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

    name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBaseModel):
    """
    Схемы для чтения данных о категории товара
    """

    id: int = Field(
        description="ID категории товара",
    )


class CategoryListBaseModel(CategoryBaseModel):
    """
    Базовая модель для схемы чтения списка категорий товара
    """

    products_count: int = Field(
        description="Количество товаров в категории",
    )


class CategoryListBoat(CategoryListBaseModel):
    """
    Список всех товаров в категории катера и их количество.
    """

    products_preview: list["BoatSummarySchema"] = Field(
        description="Превью товаров в категории",
    )


class CategoryListOutboardMotor(CategoryListBaseModel):
    """
    Список всех товаров в категории лодочные моторы и их количество.
    """

    products_preview: list["OutboardMotorSummarySchema"] = Field(
        description="Превью товаров в категории",
    )


class CategoryListTrailer(CategoryListBaseModel):
    """
    Список всех товаров в категории прицепы и их количество.
    """

    products_preview: list["TrailerSummarySchema"] = Field(
        description="Превью товаров в категории",
    )
