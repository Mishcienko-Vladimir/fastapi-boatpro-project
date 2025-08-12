from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import TrailerService

from core.config import settings
from core.schemas.products import TrailerRead, TrailerUpdate, TrailerCreate
from core.models import db_helper


router = APIRouter(prefix=settings.api.v1.trailers, tags=["Прицепы"])


@router.post("/", status_code=201, response_model=TrailerRead)
async def create_trailer(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_data: TrailerCreate,
    images: list[UploadFile] = File(...),
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.create_trailer(trailer_data, images)


@router.get("/trailer-name/{name_trailer}", status_code=200, response_model=TrailerRead)
async def get_trailer_by_name(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    name_trailer: str,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.get_trailer_by_name(name_trailer)


@router.get("/trailer-id/{trailer_id}", status_code=200, response_model=TrailerRead)
async def get_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.get_trailer_by_id(trailer_id)


@router.get("/", status_code=200, response_model=list[TrailerRead])
async def get_trailers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[TrailerRead]:
    _service = TrailerService(session)
    return await _service.get_trailers()


@router.patch("/{trailer_id}", status_code=200, response_model=TrailerRead)
async def update_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
    trailer_data: TrailerUpdate,
) -> TrailerRead:
    _service = TrailerService(session)
    return await _service.update_trailer_by_id(trailer_id, trailer_data)


@router.delete("/{trailer_id}", status_code=204)
async def delete_trailer_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trailer_id: int,
) -> None:
    _service = TrailerService(session)
    return await _service.delete_trailer_by_id(trailer_id)
