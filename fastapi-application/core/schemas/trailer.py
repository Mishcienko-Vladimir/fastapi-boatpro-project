from pydantic import BaseModel, ConfigDict, Field


class TrailerCreate(BaseModel):
    """Схемы для создания трейлера"""

    model_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название модели прицепа",
    )
    full_mass: int = Field(
        ...,
        gt=0,
        lt=32767,
        description="Полный вес прицепа в кг",
    )
    load_capacity: int = Field(
        ...,
        gt=0,
        lt=32767,
        description="Грузоподъемность в кг",
    )
    trailer_length: int = Field(
        ...,
        gt=0,
        lt=32767,
        description="Длина прицепа в мм",
    )
    max_ship_length: int = Field(
        ...,
        gt=0,
        lt=32767,
        description="Максимальная длина перевозимого судна в мм",
    )
    description: str = Field(
        default="",
        min_length=0,
        max_length=1000,
        description="Описание прицепа",
    )
    price: int = Field(
        ...,
        gt=0,
        description="Цена прицепа в рублях",
    )
    image_id: int = Field(
        default=0,
        ge=0,
        description="ID изображения прицепа",
    )

    model_config = ConfigDict(from_attributes=True)
