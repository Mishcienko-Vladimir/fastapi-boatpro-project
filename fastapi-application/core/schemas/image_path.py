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
    trailer_id: int | None = Field(
        description="ID прицепа",
    )
    boat_id: int | None = Field(
        description="ID лодки",
    )
    outboard_motor_id: int | None = Field(
        description="ID мотора",
    )


class ImagePathCreate(ImagePathBaseModel):
    """
    Схемы для создания новому пути к изображению.
    """

    pass


class ImagePathUpdate(ImagePathBaseModel):
    """
    Схемы для обновления данных пути к изображению.
    """

    path: str | None = None
    trailer_id: int | None = None
    boat_id: int | None = None
    outboard_motor_id: int | None = None


class ImagePathRead(ImagePathBaseModel):
    """
    Схемы для чтения данных пути к изображению.
    """

    id: int = Field(
        description="ID категории товара",
    )
