from fastapi import APIRouter, Depends

from core.config import settings
from core.schemas.products import TrailerRead

# from api.api_v1.services.products.trailers import TrailerService


router = APIRouter(prefix=settings.api.v1.trailers, tags=["Прицепы"])


# @router.get("/{name}", response_model=TrailerRead)
# async def get_trailer_by_name(
#     name: str,
#     service: TrailerService = Depends(),
# ):
#     return await service.get_trailer_by_name(name)


# @router.post("/", response_model=TrailerCreate)
# async def create_trailer(
#     trailer_data: TrailerCreate,
#     trailers_service: TrailerService = Depends(),
# ):
#     new_trailer = await trailers_service.create_trailer(trailer_data)
#     return new_trailer
