from fastapi_users import schemas
from pydantic import BaseModel, Field

from core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserCreate(schemas.BaseUserCreate):

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserUpdate(schemas.BaseUserUpdate):

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int
