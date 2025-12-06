import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker

from api.api_v1.services.pickup_points_service import PickupPointsService

from core.schemas.pickup_point import (
    PickupPointCreate,
    PickupPointUpdate,
    PickupPointRead,
)
from core.models.orders.order import Order


faker = Faker()
