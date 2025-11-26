from typing import Annotated
from fastapi import APIRouter, Depends, status

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.favorites_service import FavoritesService
from utils.key_builder import universal_list_key_builder

from core.config import settings
from core.dependencies import get_db_session
from core.schemas.user import UserFavorites
from core.schemas.favorite import FavoriteCreate, FavoriteRead


router = APIRouter(
    prefix=settings.api.v1.favorites,
    tags=["Избранное 💖"],
)


@router.post(
    path="/",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="add_to_favorites",
    summary="Добавление товара в избранное",
    responses={
        201: {"model": FavoriteRead},
        400: {"description": "Товар уже в избранном или данные некорректны."},
        404: {"description": "Пользователь или товар не найден."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def add_to_favorites(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    favorite_data: FavoriteCreate,
) -> FavoriteRead:
    """
    ## Добавление товара в избранное.

    **Описание:**
    Используется при нажатии кнопки «В избранное» на странице товара.

    **Принимает поля:**
    - `user_id`: ID пользователя (int, id > 0).
    - `product_id`: ID товара (int, id > 0).

    **Ответы:**
    - `201 Created` — товар успешно добавлен в избранное. Возвращает объект избранного.
    - `400 Bad Request` — товар уже в избранном.
    - `404 Not Found` — пользователь или товар не найдены.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = FavoritesService(session=session)
    create_favorite = await _service.create_favorite(favorite_data=favorite_data)
    await FastAPICache.clear(namespace=settings.cache.namespace.favorites_list)
    return create_favorite


@router.get(
    path="/",
    response_model=UserFavorites,
    status_code=status.HTTP_200_OK,
    operation_id="get_favorites",
    summary="Получение всех избранных товаров пользователя",
    responses={
        200: {"model": UserFavorites},
        404: {"description": "Пользователь не найден."},
        422: {"description": "Некорректный формат user_id."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
@cache(
    expire=60,
    key_builder=universal_list_key_builder,  # type: ignore
    namespace=settings.cache.namespace.favorites_list,
)
async def get_favorites(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: int,
) -> UserFavorites:
    """
    ## Получение всех избранных товаров пользователя.

    **Описание:**
    Используется для отображения списка избранных товаров на странице «Избранное».

    **Принимает поле:**
    - `user_id`: ID пользователя (int, id > 0).

    **Ответы:**
    - `200 OK` — список найден. Возвращает список избранных товаров с краткой информацией и изображением.
    - `404 Not Found` — пользователь не найден.
    - `422 Unprocessable Entity` — некорректный формат `user_id`.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = FavoritesService(session=session)
    return await _service.get_favorites(user_id=user_id)


@router.delete(
    path="/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_favorite_by_id",
    summary="Удаление товара из избранного",
    responses={
        204: {"description": "Товар успешно удалён из избранного."},
        404: {"description": "Избранное с таким id не найдено."},
        422: {"description": "Некорректный формат favorite_id."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def delete_favorite_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    favorite_id: int,
) -> None:
    """
    ## Удаление товара из избранного.

    **Описание:**
    Используется для удаления товара из избранного по его ID.

    **Принимает поле:**
    - `favorite_id`: ID записи в избранном (int, id > 0).

    **Ответы:**
    - `204 No Content` — товар успешно удалён. Ничего не возвращается.
    - `404 Not Found` — запись в избранном не найдена.
    - `422 Unprocessable Entity` — некорректный формат `favorite_id`.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = FavoritesService(session=session)
    delete_favorite = await _service.delete_favorite_by_id(favorite_id=favorite_id)
    await FastAPICache.clear(namespace=settings.cache.namespace.favorites_list)
    return delete_favorite
