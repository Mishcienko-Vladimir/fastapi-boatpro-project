from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import CategoryService

from core.schemas.products import CategoryCreate, CategoryRead, CategoryUpdate
from core.dependencies import get_db_session


router = APIRouter(tags=["Каталог 📋"])


@router.post(
    path="/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_category",
    summary="Создание новой категории",
    responses={
        201: {"model": CategoryRead},
        400: {"description": "Категория с таким именем уже существует."},
        422: {"description": "Ошибка валидации входных данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def create_category(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_data: CategoryCreate,
) -> CategoryRead:
    """
    ## Создание новой категории.

    **Описание:**
    Используется в админ-панели для добавления новой категории товаров (например, "Катера", "Лодочные моторы").

    **Принимает поля:**
    - `name`: Название категории (str, 1–50 символов, уникальное).
    - `description`: Описание категории (str, необязательное поле, может быть пустым).

    **Ответы:**
    - `201 Created` — категория успешно создана. Возвращает созданную категорию.
    - `400 Bad Request` — категория с таким именем уже существует.
    - `422 Unprocessable Entity` — ошибка валидации (например, имя слишком длинное).
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.create_category(category_data=category_data)


@router.get(
    path="/category-name/{name_category}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_category_by_name",
    summary="Получение категории по названию",
    responses={
        200: {"model": CategoryRead},
        404: {"description": "Категория не найдена."},
        422: {"description": "Некорректный формат имени категории."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_category_by_name(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    name_category: str,
) -> CategoryRead:
    """
    ## Получение категории по названию.

    **Описание:**
    Используется для отображения категории по её имени (например, в фильтрах или админке).

    **Принимает поле:**
    - `name_category`: Название категории (str, 1–50 символов).

    **Ответы:**
    - `200 OK` — категория найдена. Возвращает объект категории.
    - `404 Not Found` — категория с таким именем не найдена.
    - `422 Unprocessable Entity` — некорректный формат имени.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.get_category_by_name(name_category=name_category)


@router.get(
    path="/category-id/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    operation_id="get_category_by_id",
    summary="Получение категории по id",
    responses={
        200: {"model": CategoryRead},
        404: {"description": "Категория не найдена."},
        422: {"description": "Некорректный формат id."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
) -> CategoryRead:
    """
    ## Получение категории по id.

    **Описание:**
    Используется в админ-панели и на сайте для получения категории по её ID.

    **Принимает поле:**
    - `category_id`: ID категории (int, целое число).

    **Ответы:**
    - `200 OK` — категория найдена. Возвращает объект категории.
    - `404 Not Found` — категория не найдена.
    - `422 Unprocessable Entity` — некорректный формат ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.get_category_by_id(category_id=category_id)


@router.get(
    path="/",
    response_model=list[CategoryRead],
    status_code=status.HTTP_200_OK,
    operation_id="get_categories",
    summary="Получение всех категорий",
    responses={
        200: {"model": list[CategoryRead]},
        404: {"description": "Список категорий пуст."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def get_categories(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[CategoryRead]:
    """
    ## Получение всех категорий.

    **Описание:**
    Используется для отображения списка категорий в админ-панели, на сайте и в фильтрах.

    **Ответы:**
    - `200 OK` — список найден. Возвращает список категорий.
    - `404 Not Found` — нет ни одной категории.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.get_categories()


@router.patch(
    path="/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    operation_id="update_category_by_id",
    summary="Частичное обновление категории по id",
    responses={
        200: {"model": CategoryRead},
        400: {"description": "Категория с таким именем уже существует."},
        404: {"description": "Категория не найдена."},
        422: {"description": "Ошибка валидации данных."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def update_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
    category_data: CategoryUpdate,
) -> CategoryRead:
    """
    ## Частичное обновление категории по id.

    **Описание:**
    Используется в админ-панели для редактирования категории.

    **Принимает поля:**
    - `category_id`: ID категории (int, целое число).
    - `name`: Новое название (str, 1–50 символов, уникальное). Если не указано — не меняется.
    - `description`: Новое описание (str, необязательное). Если не указано — не меняется.

    **Ответы:**
    - `200 OK` — категория успешно обновлена. Возвращает обновлённую категорию.
    - `400 Bad Request` — имя уже занято.
    - `404 Not Found` — категория не найдена.
    - `422 Unprocessable Entity` — ошибка валидации.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.update_category_by_id(
        category_id=category_id,
        category_data=category_data,
    )


@router.delete(
    path="/{category_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_category_by_id",
    summary="Удаление категории по id",
    responses={
        204: {"description": "Категория успешно удалена."},
        404: {"description": "Категория не найдена."},
        422: {"description": "Некорректный формат ID."},
        500: {"description": "Внутренняя ошибка сервера."},
    },
)
async def delete_category_by_id(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    category_id: int,
) -> None:
    """
    ## Удаление категории по id.

    **Описание:**
    Используется в админ-панели для удаления категории.
    ⚠️ Удаление возможно только если в категории нет товаров.

    **Принимает поле:**
    - `category_id`: ID категории (int, целое число), для удаления.

    **Ответы:**
    - `204 No Content` — категория успешно удалена. Ответ пуст.
    - `404 Not Found` — категория не найдена.
    - `422 Unprocessable Entity` — некорректный ID.
    - `500 Internal Server Error` — внутренняя ошибка сервера.
    """
    _service = CategoryService(session=session)
    return await _service.delete_category_by_id(category_id=category_id)
