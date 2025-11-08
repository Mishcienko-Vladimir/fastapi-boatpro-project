from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products.products_service import ProductsService

from core.config import settings
from core.dependencies import get_db_session
from core.models.products import Product
from core.schemas.products import ProductBaseModelRead


router = APIRouter(prefix=settings.api.v1.search, tags=["Поиск 🔍"])


@router.get("/", response_model=list[ProductBaseModelRead])
async def search_products(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    query: str,
) -> list[ProductBaseModelRead]:
    """
    Поиск товаров по ключевому слову (название, производитель, описание).
    """
    _service = ProductsService(session, Product)
    products = await _service.get_search_products(query)

    return [
        ProductBaseModelRead.model_validate(
            {
                **product.__dict__,
                "image": product.images[0] if product.images else None,
            }
        )
        for product in products
    ]
