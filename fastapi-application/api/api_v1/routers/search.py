from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products.products_service import ProductsService

from core.config import settings
from core.dependencies import get_db_session
from core.models.products import Product
from core.schemas.products import ProductBaseModelRead


router = APIRouter(
    prefix=settings.api.v1.search,
    tags=["Поиск 🔍"],
)


@router.get(
    path="/",
    response_model=list[ProductBaseModelRead],
    status_code=status.HTTP_200_OK,
    operation_id="search_products",
    summary="Поиск товаров по ключевому слову",
    responses={
        200: {"model": list[ProductBaseModelRead]},
        500: {"description": "Внутренняя ошибка сервера"},
    },
)
async def search_products(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    query: str,
) -> list[ProductBaseModelRead]:
    """
    ## Поиск товаров по ключевому слову.

    **Описание:**
    Используется для поиска товаров по совпадению в полях:
    - `название`
    - `производитель`
    - `описание`

    **Принимает параметр:**
    - `query`: Строка поиска (str, минимум 1 символ).

    **Ответы:**
    - `200 OK` — найдены товары. Возвращает список товаров с краткой информацией и одним изображением.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = ProductsService(session=session, product_db=Product)
    products = await _service.get_search_products(query=query)
    return [
        ProductBaseModelRead.model_validate(
            {
                **product.__dict__,
                "image": product.images[0] if product.images else None,
            }
        )
        for product in products
    ]
