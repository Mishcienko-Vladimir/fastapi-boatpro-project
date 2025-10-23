from typing import Annotated, Optional

from fastapi import Form, HTTPException, File, UploadFile
from fastapi import APIRouter, Request, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.routers.products.trailers import (
    get_trailers,
    create_trailer,
    update_trailer_data_by_id,
    update_trailer_images_by_id,
    delete_trailer_by_id,
)

from core.repositories.authentication.fastapi_users import current_active_superuser
from core.config import settings
from core.models import User, db_helper
from core.schemas.products.trailer import TrailerUpdate

from utils.templates import templates


router = APIRouter(prefix=settings.view.trailers)
