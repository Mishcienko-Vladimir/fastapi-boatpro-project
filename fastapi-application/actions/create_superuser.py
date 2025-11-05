import asyncio
import logging
import contextlib

from os import getenv
from typing import Optional
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.dependencies.authentication import get_users_db
from api.api_v1.dependencies.authentication import get_user_manager

from core.repositories.authentication.user_manager import UserManager
from core.models import db_helper, User
from core.schemas.user import UserCreate
from core.config import settings


log = logging.getLogger(__name__)

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(
    lambda db, _: get_user_manager(db, BackgroundTasks())
)

default_email = getenv("DEFAULT_EMAIL", f"{settings.admin.admin_email}")
default_password = getenv("DEFAULT_PASSWORD", f"{settings.admin.admin_password}")
default_first_name = getenv("DEFAULT_FIRST_NAME", "Admin")
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    email: str = default_email,
    password: str = default_password,
    first_name: str = default_first_name,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        first_name=first_name,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db, None) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


async def create_superuser_if_not_exists(
    session: AsyncSession,
    email: str = default_email,
    password: str = default_password,
    first_name: str = default_first_name,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
) -> Optional[User]:
    """
    Создаёт суперпользователя, если его ещё нет.
    Использует email и password из настроек.
    """

    async with get_users_db_context(session) as users_db:
        async with get_user_manager_context(users_db, None) as user_manager:
            # Проверяем, существует ли пользователь
            user = await user_manager.user_db.get_by_email(email)
            if user is not None:
                if user.is_superuser:
                    return user
                else:
                    log.info("Создан Суперпользователь.")
                    log.warning(
                        "Пользователь с email: %r существует, но не является суперпользователем.",
                        email,
                    )
                    return None

            user_create = UserCreate(
                email=email,
                password=password,
                first_name=first_name,
                is_active=is_active,
                is_superuser=is_superuser,
                is_verified=is_verified,
            )
            user = await create_user(user_manager=user_manager, user_create=user_create)
            log.info("Создан Суперпользователь.")
            return user


if __name__ == "__main__":
    asyncio.run(create_superuser())
