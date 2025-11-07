# Создание FastAPI приложения и переопределение пути загрузки статики
from contextlib import asynccontextmanager
from redis.asyncio import Redis

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from slowapi.middleware import SlowAPIMiddleware

from actions.create_superuser import create_superuser_if_not_exists
from api.webhooks import webhooks_router
from core.models import db_helper
from core.config import settings, BASE_DIR
from errors_handlers import register_errors_handlers
from utils.limiter import limiter

from middleware.custom_rate_limit_middleware import CustomRateLimitMiddleware
from middleware.security_headers_middleware import SecurityHeadersMiddleware


# Для закрытия базы данных
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )
    # Создание суперпользователя при старте, если его нет.
    async with db_helper.session_factory() as session:
        await create_superuser_if_not_exists(session)

    yield
    # shutdown
    await db_helper.dispose()


def register_static_docs_routes(app: FastAPI):
    """
    Создание статических URL для Swagger, ReDoc и статических файлов.
    Необходимо для того, чтобы документация нормально открывалась.
    """

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )


def create_app(
    create_custom_static_urls: bool = False,
    lifespan_override=None,
) -> FastAPI:
    """Создание FastAPI приложения."""

    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan_override or lifespan,
        docs_url=None if create_custom_static_urls else "/docs",
        redoc_url=None if create_custom_static_urls else "/redoc",
        webhooks=webhooks_router,
    )

    # Защита от спама (bruteforce).
    app.state.limiter = limiter  # type: ignore
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(CustomRateLimitMiddleware)

    # Установка безопасности HTTP-заголовков.
    app.add_middleware(SecurityHeadersMiddleware)

    # Добавления CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Создание статических URL для Swagger, ReDoc.
    if create_custom_static_urls:
        register_static_docs_routes(app)

    # Регистрация статических файлов в папке static.
    app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

    # Регистрация обработчиков ошибок из модуля errors_handlers
    register_errors_handlers(app)
    return app
