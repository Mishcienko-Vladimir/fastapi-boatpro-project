from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.outboard_motors import (
    get_outboard_motors,
    create_outboard_motor,
    update_outboard_motor_data_by_id,
    update_outboard_motor_images_by_id,
    delete_outboard_motor_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.outboard_motor import OutboardMotorUpdate

from utils.templates import templates


router = APIRouter(prefix=settings.view.outboard_motors)
