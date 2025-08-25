from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, BackgroundTasks

from core.repositories.authentication.user_manager import UserManager
from .users import get_users_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase  # noqa


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_users_db)],
    background_tasks: BackgroundTasks,
):
    yield UserManager(
        user_db,
        background_tasks=background_tasks,
    )
