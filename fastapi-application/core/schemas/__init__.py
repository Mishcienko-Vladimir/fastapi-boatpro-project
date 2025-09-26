__add__ = (
    "BaseSchemaModel",
    "FavoriteCreate",
    "FavoriteRead",
    "UserRegisteredNotification",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserFavorites",
)

from .base_model import BaseSchemaModel
from .favorite import FavoriteCreate, FavoriteRead
from .user import (
    UserRegisteredNotification,
    UserCreate,
    UserUpdate,
    UserRead,
    UserFavorites,
)
