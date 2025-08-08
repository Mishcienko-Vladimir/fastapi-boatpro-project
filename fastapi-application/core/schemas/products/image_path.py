from fastapi import UploadFile
from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


class ImagePathBaseModel(BaseSchemaModel):
    """
    Базовая схема для пути к изображению.
    """

    path: str = Field(
        min_length=1,
        max_length=255,
        description="Путь к изображению",
    )


class ImagePathCreate(ImagePathBaseModel):
    """
    Схема для создания новому пути к изображению.
    """

    pass


class ImagePathUpdate(ImagePathBaseModel):
    """
    Схема для обновления новых и удаления старых изображений.
    """

    remove_images: set[int] = Field(
        description="Id изображений, для удаления",
    )
    add_images: list[UploadFile] = Field(
        description="Новые изображения",
    )


class ImagePathRead(ImagePathBaseModel):
    """
    Схема для чтения пути к изображению.
    """

    id: int = Field(
        description="ID категории товара",
    )
