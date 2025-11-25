from fastapi_users import schemas
from pydantic import BaseModel, Field

from core.types.user_id import UserIdType
from .favorite import FavoriteRead


class UserCreate(schemas.BaseUserCreate):
    """Схема создания пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserRead(schemas.BaseUser[UserIdType]):
    """Схема для чтения пользователя"""

    first_name: str = Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя",
    )


class UserRegisteredNotification(BaseModel):
    """Схема уведомление о регистрации пользователя"""

    user: UserRead = Field(
        description="Пользователь",
    )
    ts: int = Field(
        description="Время регистрации",
    )


class UserFavorites(BaseModel):
    """Схема списка избранных товаров пользователя"""

    favorites: list[FavoriteRead] = Field(
        description="Список избранных товаров",
    )
