from fastapi import APIRouter

from core.config import settings


router = APIRouter(prefix=settings.api.v1.trailers, tags=["Прицепы"])


@router.get("/")
def get_trailers():
    return {"message": "Hello, World!"}
