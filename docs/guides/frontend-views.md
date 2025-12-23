## Создание и инициализация Views 

В `core/config.py` добавьте префикс для views гидроциклов:
```python
class ViewPrefix(BaseModel):
    """Конфигурация префикса для страниц"""

    ...
    jet_skis: str = "/jet-skis"
```
Создайте модуль `jet_skis.py` в `views/products`, для представления HTML-страниц, связанных с гидроциклами — 
таких, как каталог и детальная страница товара:
```python
from typing import Optional, Annotated
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.jet_skis import get_jet_skis_summary, get_jet_ski_by_name
from core.dependencies import get_db_session
from core.dependencies.fastapi_users import optional_user
from core.config import settings
from core.models import User
from utils.templates import templates

router = APIRouter(prefix=settings.view.jet_skis)

@router.get(
    path="/",
    name="jet_skis",
    include_in_schema=False,
    response_model=None,
)
async def jet_skis(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    jet_skis_list = await get_jet_skis_summary(session=session)
    return templates.TemplateResponse(
        request=request,
        name="products/jet-skis.html",
        context={
            "jet_skis_list": jet_skis_list,
            "user": user,
        },
    )

@router.get(
    path=f"/{{jet_ski_name}}",
    name="jet_ski_detail",
    include_in_schema=False,
    response_model=None,
)
async def jet_ski_detail(
    request: Request,
    jet_ski_name: str,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Optional[User] = Depends(optional_user),
):
    jet_ski = await get_jet_ski_by_name(session=session, jet_ski_name=jet_ski_name)
    return templates.TemplateResponse(
        request=request,
        name="products/jet-ski-detail.html",
        context={
            "jet_ski": jet_ski,
            "user": user,
        },
    )
```
Инициализируйте его в `views/products/__init__.py`:
```python
...
from .jet_skis import router as jet_skis_router

router = APIRouter(prefix=settings.view.catalog)

router.include_router(jet_skis_router)
...
```
Создайте модуль `jet_skis.py` в `views/admin`, для представления административной HTML-страницы, позволяющий управлять 
гидроциклами — просматривать, редактировать и удалять товары через веб-интерфейс.
```python
from typing import Annotated, Optional
from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.jet_skis import (
    get_jet_skis,
    create_jet_ski,
    update_jet_ski_data_by_id,
    update_jet_ski_images_by_id,
    delete_jet_ski_by_id,
)
from api.api_v1.dependencies.create_multipart_form_data import create_multipart_form_data
from core.dependencies import get_db_session
from core.dependencies.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User
from core.schemas.products.jet_ski import JetSkiUpdate, JetSkiCreate
from utils.templates import templates

router = APIRouter(prefix=settings.view.jet_skis)

@router.get(
    path="/",
    name="admin_jet_skis",
    include_in_schema=False,
    response_model=None,
)
async def admin_jet_skis(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User,Depends(current_active_superuser)],
):
    jet_skis_list = await get_jet_skis(session=session)
    return templates.TemplateResponse(
        request=request,
        name="admin/jet-skis.html",
        context={
            "user": user,
            "jet_skis_list": jet_skis_list,
        },
    )

@router.post(
    path="/delete-jet-ski",
    name="admin_delete_jet_ski",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_jet_ski(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_superuser)],
    jet_ski_id_del: int = Form(...),
):
    try:
        await delete_jet_ski_by_id(session=session, jet_ski_id=jet_ski_id_del)
        message = f"Гидроцикл с ID {jet_ski_id_del} успешно удален"
    except HTTPException as exc:
        message = exc.detail

    return templates.TemplateResponse(
        request=request,
        name="admin/jet-skis.html",
        context={
            "user": user,
            "jet_skis_list": await get_jet_skis(session=session),
            "message": message,
        },
    )

@router.post(
    path="/create-jet-ski",
    name="admin_create_jet_ski",
    include_in_schema=False,
    response_model=None,
)
async def admin_create_jet_ski(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_superuser)],
    jet_ski_data: Annotated["JetSkiCreate", Depends(create_multipart_form_data(JetSkiCreate))],
    images: Annotated[list[UploadFile], File(...)],
):
    try:
        response = await create_jet_ski(
            session=session,
            jet_ski_data=jet_ski_data,
            images=images,
        )
        message = f"Гидроцикл с ID {response.id} успешно создан"
    except HTTPException as exc:
        message = f"Гидроцикл с именем {jet_ski_data.name} уже существует"
    except Exception as exc:
        message = f"Ошибка при создании гидроцикла: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/jet-skis.html",
        context={
            "user": user,
            "jet_skis_list": await get_jet_skis(session=session),
            "message": message,
        },
    )

@router.post(
    path="/update-jet-ski",
    name="admin_update_jet_ski",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_jet_ski(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_superuser)],
    jet_ski_id_up: int = Form(...),
    name: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    length_hull: Optional[str] = Form(None),
    width_hull: Optional[str] = Form(None),
    weight: Optional[str] = Form(None),
    capacity: Optional[int] = Form(None),
    load_capacity: Optional[int] = Form(None),
    engine_power: Optional[int] = Form(None),
    engine_displacement: Optional[int] = Form(None),
    fuel_capacity: Optional[int] = Form(None),
    hull_material: Optional[str] = Form(None),
    gasoline_brand: Optional[int] = Form(None),
):
    try:
        update_data = {}
        for key, value in locals().items():
            if (
                key not in ["request", "session", "user", "jet_ski_id_up"]
                and value is not None
            ):
                if isinstance(value, str) and value.strip() == "":
                    continue
                try:
                    numeric_value = int(value)
                    update_data[key] = numeric_value
                except (ValueError, TypeError):
                    update_data[key] = value

        if not update_data:
            message = "Нет данных для обновления"

        jet_ski_update = JetSkiUpdate(**update_data)
        updated_jet_ski = await update_jet_ski_data_by_id(
            session=session,
            jet_ski_id=jet_ski_id_up,
            jet_ski_data=jet_ski_update,
        )
        message = f"Гидроцикл с ID {jet_ski_id_up} успешно обновлен"
    except HTTPException as exc:
        message = f"Гидроцикл с ID {jet_ski_id_up} не найден"
    except Exception as exc:
        message = f"Ошибка при обновлении гидроцикла: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/jet-skis.html",
        context={
            "user": user,
            "jet_skis_list": await get_jet_skis(session=session),
            "message": message,
        },
    )

@router.post(
    path="/update-images",
    name="admin_update_jet_ski_images",
    include_in_schema=False,
    response_model=None,
)
async def admin_update_jet_ski_images(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[User, Depends(current_active_superuser)],
    jet_ski_id_img: int = Form(...),
    remove_images: str | None = Form(None),
    add_images: list[UploadFile] = File(...),
):
    try:
        await update_jet_ski_images_by_id(
            session=session,
            jet_ski_id=jet_ski_id_img,
            remove_images=remove_images,
            add_images=add_images,
        )
        message = f"Фото гидроцикла с ID {jet_ski_id_img} успешно обновлены"
    except HTTPException as exc:
        message = exc.detail
    except Exception as exc:
        message = f"Ошибка при обновлении фото: {str(exc)}"

    return templates.TemplateResponse(
        request=request,
        name="admin/jet-skis.html",
        context={
            "user": user,
            "jet_skis_list": await get_jet_skis(session=session),
            "message": message,
        },
    )
```
Инициализируйте его в `views/admin/__init__.py`:
```python
...
from .jet_skis import router as jet_skis_router

router = APIRouter(prefix=settings.view.admin)

router.include_router(jet_skis_router)
...
```

## ✅ Итог

**Созданные views-представления:**
- `views/products/jet_skis.py`
- `views/admin/jet_skis.py`

**Инициализация views в:**
- `views/products/__init__.py`
- `views/admin/__init__.py`

---
[← Назад в README](../../../../)