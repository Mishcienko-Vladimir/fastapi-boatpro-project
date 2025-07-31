from pydantic import Field

from core.schemas.base_model import BaseSchemaModel


class ProductBaseModel(BaseSchemaModel):
    """
    Базовая модель для товаров.
    """

    model_name: str = Field(
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
    image_id: list[int] = Field(
        description="ID изображения",
    )
    is_active: bool = Field(
        description="Наличие товара",
    )


class ProductCreateBaseModel(ProductBaseModel):
    """
    Абстрактная модель создания товаров для product_manager_crud.
    """

    pass


class ProductUpdateBaseModel(ProductCreateBaseModel):
    """
    Абстрактная модель обновления товаров для product_manager_crud.
    """

    model_name: str | None = None
    price: int | None = None
    company_name: str | None = None
    description: str | None = None
    image_id: int | None = None
    is_active: bool | None = None
