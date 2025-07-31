__all__ = (
    "ProductBaseModel",
    "ProductTypeCreate",
    "ProductTypeUpdate",
    "ProductTypeRead",
    "BoatCreate",
    "BoatUpdate",
    "BoatRead",
    "OutboardMotorCreate",
    "OutboardMotorUpdate",
    "OutboardMotorRead",
    "TrailerCreate",
    "TrailerUpdate",
    "TrailerRead",
)

from .product_base_model import (
    ProductBaseModel,
)
from .product_type import (
    ProductTypeCreate,
    ProductTypeUpdate,
    ProductTypeRead,
)
from .boat import (
    BoatCreate,
    BoatUpdate,
    BoatRead,
)
from .motor import (
    OutboardMotorCreate,
    OutboardMotorUpdate,
    OutboardMotorRead,
)
from .trailer import (
    TrailerCreate,
    TrailerUpdate,
    TrailerRead,
)
