from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


class ImagePathBaseModel(BaseSchemaModel):
    """Базовая схема для путей к изображениям."""

    path: str = Field(
        min_length=1,
        max_length=255,
        description="Путь к изображению",
    )


class ImagePathCreate(ImagePathBaseModel):
    """Схема создания нового пути к изображению."""

    pass


class ImagePathRead(ImagePathBaseModel):
    """Схема для чтения пути к изображению."""

    id: int = Field(
        description="ID категории товара",
    )
