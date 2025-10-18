# Обработчик ошибок
import logging

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import ORJSONResponse

from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError

from utils.templates import templates


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
    def http_exception_handler(request: Request):
        return templates.TemplateResponse(
            name="page-missing.html",
            context={
                "request": request,
                "user": None,
            },
        )
