from typing import Annotated
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.services.products import ProductsService

from core.dependencies import get_db_session, current_active_superuser
from core.config import settings
from core.models import User
from core.models.products import Product
from core.schemas.products import ProductBaseModelRead

from utils.templates import templates


router = APIRouter(prefix=settings.view.home)


@router.get(
    "/",
    name="admin_home",
    include_in_schema=False,
    response_model=None,
)
async def admin_home(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    all_products = await ProductsService(
        session=session,
        product_db=Product,
    ).get_products()
    products_list = [
        ProductBaseModelRead.model_validate(product) for product in all_products
    ]
    number_boats = sum(1 for boat in products_list if boat.type_product == "boat")
    number_outboard_motors = sum(
        1
        for outboard_motor in products_list
        if outboard_motor.type_product == "outboard_motor"
    )
    number_trailers = sum(
        1 for trailer in products_list if trailer.type_product == "trailer"
    )
    return templates.TemplateResponse(
        request=request,
        name="admin/home.html",
        context={
            "user": user,
            "products_list": products_list,
            "number_boats": number_boats,
            "number_outboard_motors": number_outboard_motors,
            "number_trailers": number_trailers,
        },
    )
