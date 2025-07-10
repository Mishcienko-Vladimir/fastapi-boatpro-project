from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from core.config import settings
from core.models import User
from core.schemas.user import UserRead


router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)
