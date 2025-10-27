from fastapi import APIRouter
from typing import (
    Annotated,
)
from fastapi import APIRouter, Depends, Response, Request
from api.api_v1.dependencies.authentication import get_users_db
from core.repositories.authentication.fastapi_users import fastapi_users

from core.config import settings
from core.models.user import SQLAlchemyUserDatabase
from core.schemas.user import UserRead, UserUpdate


router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])


@router.get(
    "",
    response_model=list[UserRead],
)
async def get_users_list(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ],
) -> list[UserRead]:
    users = await users_db.get_users()
    return [UserRead.model_validate(user) for user in users]


# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
