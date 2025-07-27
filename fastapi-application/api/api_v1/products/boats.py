from fastapi import APIRouter

from core.config import settings


router = APIRouter(prefix=settings.api.v1.boats, tags=["Катера"])


@router.get("/")
def get_boats():
    return {"message": "Hello, World!"}
