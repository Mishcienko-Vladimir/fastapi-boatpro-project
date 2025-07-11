from contextlib import asynccontextmanager

import uvicorn
import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core.config import settings
from core.models import db_helper


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


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
main_app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host=settings.run.host, port=settings.run.port, reload=True
    )
