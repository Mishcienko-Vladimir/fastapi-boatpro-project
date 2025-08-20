from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, File

from api.api_v1.services.products import ProductsService

from core.config import settings
from core.models import db_helper
from core.models.products import OutboardMotor
from core.schemas.products import (
    EngineType,
    OutboardMotorRead,
    OutboardMotorUpdate,
    OutboardMotorCreate,
)


router = APIRouter(prefix=settings.api.v1.outboard_motors, tags=["Лодочные моторы"])
