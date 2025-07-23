from datetime import datetime
from typing import Optional
from pydantic import Field

from core.schemas.base import BaseSchema


class MotorBase(BaseSchema):
    """
    Базовая схема для лодочных моторов
    """

    company_name: str = Field(
        min_length=1,
        max_length=255,
        description="Название производителя",
    )
    engine_power: int = Field(
        gt=0,
        lt=1000,
        description="Мощность двигателя в л.с.",
    )
    price: int = Field(
        gt=0,
        description="Цена мотора в рублях",
    )
    weight: int = Field(
        gt=0,
        lt=1000,
        description="Вес мотора в кг",
    )
    description: str = Field(
        min_length=0,
        description="Описание мотора",
    )
    image_id: int = Field(
        ge=0,
        description="ID изображения мотора",
    )


class MotorCreate(MotorBase):
    """
    Схема для создания нового мотора
    """

    pass


class MotorUpdate(MotorBase):
    """
    Схема для обновления дынных мотора
    """

    company_name: Optional[str]
    engine_power: Optional[int]
    price: Optional[int]
    weight: Optional[int]
    description: Optional[str]
    image_id: Optional[int]
