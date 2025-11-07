from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.favorites_service import FavoritesService
from utils.key_builder import universal_list_key_builder

from core.config import settings
from core.models import db_helper
from core.schemas.user import UserFavorites
from core.schemas.favorite import FavoriteCreate, FavoriteRead


router = APIRouter(prefix=settings.api.v1.favorites, tags=["Избранное 💖"])


@router.post("/", status_code=201, response_model=FavoriteRead)
async def add_to_favorites(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    favorite_data: FavoriteCreate,
) -> FavoriteRead:
    """
    Добавление товара в избранное.
    """
    _service = FavoritesService(session)
    create_favorite = await _service.create_favorite(favorite_data)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.favorites_list,
    )
    return create_favorite


@router.get("/", status_code=201, response_model=UserFavorites)
@cache(
    expire=60,
    key_builder=universal_list_key_builder,
    namespace=settings.cache.namespace.favorites_list,
)
async def get_favorites(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
) -> UserFavorites:
    """
    Получение всех избранных товаров пользователя.
    """
    _service = FavoritesService(session)
    return await _service.get_favorites(user_id)


@router.delete("/", status_code=204)
async def delete_favorite_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    favorite_id: int,
) -> None:
    """
    Удаление товара из избранного.
    """
    _service = FavoritesService(session)
    delete_favorite = await _service.delete_favorite_by_id(favorite_id)
    await FastAPICache.clear(
        namespace=settings.cache.namespace.favorites_list,
    )
    return delete_favorite
