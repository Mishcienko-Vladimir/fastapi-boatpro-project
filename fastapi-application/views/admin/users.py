from typing import Annotated

from fastapi import Form
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.users import get_users_list
from api.api_v1.dependencies.authentication.user_manager import get_user_manager

from core.config import settings
from core.dependencies import get_db_session
from core.schemas.user import UserRead

from core.models.user import SQLAlchemyUserDatabase
from core.models import User

from core.repositories.authentication.user_manager import UserManager
from core.repositories.authentication.fastapi_users import current_active_superuser

from utils.templates import templates


router = APIRouter(prefix=settings.view.users)


@router.get(
    path="/",
    name="admin_users",
    include_in_schema=False,
    response_model=None,
)
async def admin_users(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    users_list = await get_users_list(
        SQLAlchemyUserDatabase(session=session, user_table=User)
    )

    # Проверка: если элемент — это экземпляр UserRead, тогда вызываем model_dump
    users_list = [
        (
            user.model_dump() if isinstance(user, UserRead) else user
        )  # или пропуск, если ожидается dict
        for user in users_list
    ]

    number_verified = sum(
        1 for user in users_list if "is_verified" in user and user["is_verified"]
    )
    number_superuser = sum(
        1 for user in users_list if "is_superuser" in user and user["is_superuser"]
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/users.html",
        context={
            "user": user,
            "users_list": users_list,
            "number_verified": number_verified,
            "number_superuser": number_superuser,
        },
    )


@router.post(
    path="/delete-user",
    name="admin_delete_user",
    include_in_schema=False,
    response_model=None,
)
async def admin_delete_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
    user: Annotated[User, Depends(current_active_superuser)],
    user_id_del: int = Form(...),
):
    try:
        user_to_delete = await user_manager.user_db.get(user_id_del)
        if not user_to_delete:
            message = f"Пользователь с ID {user_id_del} не найден."
        else:
            await user_manager.delete(user_to_delete, request=request)
            message = f"Пользователь с ID {user_id_del} успешно удалён."

    except Exception as e:
        message = f"Ошибка при удалении: {str(e)}"

    # Обновляем список
    users_db = SQLAlchemyUserDatabase(session, User)
    users = await users_db.get_users()
    users_list = [UserRead.model_validate(u).model_dump() for u in users]
    number_verified = sum(1 for u in users_list if u["is_verified"])
    number_superuser = sum(1 for u in users_list if u["is_superuser"])

    return templates.TemplateResponse(
        request=request,
        name="admin/users.html",
        context={
            "user": user,
            "users_list": users_list,
            "number_verified": number_verified,
            "number_superuser": number_superuser,
            "message": message,
        },
    )
