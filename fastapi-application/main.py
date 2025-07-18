from contextlib import asynccontextmanager

import uvicorn
import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.webhooks import webhooks_router
from api import router as api_router
from core.config import settings
from core.models import db_helper
from views import router as views_router


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


# Для закрытия базы данных
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse, lifespan=lifespan, webhooks=webhooks_router
)
main_app.include_router(api_router)
main_app.include_router(views_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
