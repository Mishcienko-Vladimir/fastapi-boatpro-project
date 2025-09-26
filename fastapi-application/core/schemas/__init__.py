__add__ = (
    "BaseSchemaModel",
    "FavoriteModel",
    "UserRegisteredNotification",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserFavorites",
)

from .base_model import BaseSchemaModel
from .favorite import FavoriteModel
from .user import (
    UserRegisteredNotification,
    UserCreate,
    UserUpdate,
    UserRead,
    UserFavorites,
)
