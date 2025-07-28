from fastapi import APIRouter

from core.config import settings


router = APIRouter(prefix=settings.api.v1.outboard_motors, tags=["Лодочные моторы"])


@router.get("/")
def get_outboard_motors():
    return {"message": "Hello, World!"}
