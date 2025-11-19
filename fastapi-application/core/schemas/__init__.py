__add__ = (
    "BaseSchemaModel",
    "FavoriteCreate",
    "FavoriteRead",
    "OrderCreate",
    "OrderRead",
    "PickupPointCreate",
    "PickupPointUpdate",
    "PickupPointRead",
    "UserRegisteredNotification",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserFavorites",
)

from .base_model import BaseSchemaModel
from .favorite import FavoriteCreate, FavoriteRead
from .order import OrderCreate, OrderRead
from .pickup_point import PickupPointCreate, PickupPointUpdate, PickupPointRead
from .user import (
    UserRegisteredNotification,
    UserCreate,
    UserUpdate,
    UserRead,
    UserFavorites,
)
