# Обработчик ошибок
import logging

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import ORJSONResponse

from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.responses import RedirectResponse
from slowapi.errors import RateLimitExceeded


log = logging.getLogger(__name__)


def register_errors_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> ORJSONResponse:
        """Обработчик ошибок валидации данных"""

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Ошибка валидации данных",
                "error": exc.errors(),
            },
        )

    @app.exception_handler(DatabaseError)
    def handle_db_error(
        request: Request,
        exc: DatabaseError,
    ) -> ORJSONResponse:
        """Обработчик ошибок базы данных"""

        log.error(
            "Произошла ошибка базы данных",
            exc_info=exc,
        )
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Произошла непредвиденная ошибка. "
                "Администраторы уже работают над решением."
            },
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        if request.url.path.startswith("/api"):
            return ORJSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )

        if exc.status_code == 404:
            return RedirectResponse(url="/page-missing")
        if exc.status_code in (401, 403):
            return RedirectResponse(url="/page-missing")

        return RedirectResponse(url="/page-missing")

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        if request.url.path.startswith("/api"):
            return ORJSONResponse(
                status_code=429,
                content={"detail": "Слишком много запросов, попробуйте позже."},
            )

        return RedirectResponse(url="/limit-exceeded")
