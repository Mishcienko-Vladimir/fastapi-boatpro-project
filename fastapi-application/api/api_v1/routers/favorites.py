from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.favorites_service import FavoritesService

from core.config import settings
from core.models import db_helper
from core.models.favorite import Favorite
from core.schemas.favorite import FavoriteCreate, FavoriteRead


router = APIRouter(prefix=settings.api.v1.favorites, tags=["Избранное"])


@router.post("/", status_code=201, response_model=FavoriteRead)
async def add_to_favorites(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    favorite_data: FavoriteCreate,
) -> FavoriteRead:
    """
    Добавление товара в избранное.
    """
    _service = FavoritesService(session)
    return await _service.create_favorite(favorite_data)
